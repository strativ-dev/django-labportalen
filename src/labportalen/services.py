# Python import
import os
import shutil
from time import sleep
from typing import Any, Optional
import abc

# Django import
from django.conf import settings
from django.db import transaction
from django.db.models import Model
from django.apps import apps

# Thirdparty imports
import xmltodict
import pysftp

# Self import
from .constants import COMPLETED_REPLY_STATUS, PARTIAL_REPLY_STATUS
from .models import LabportalenReport


class BaseLabportalenService(metaclass=abc.ABCMeta):
    TYPE_LIST_OF_MODELS = 1

    def __init__(self) -> None:
        super().__init__()
        self.fields_config = {
            'case_model': {'required': True, 'type': Model},
        }
        if not hasattr(settings, 'LABPORTALEN_SETTINGS'):
            raise Exception("LABPORTALEN_SETTINGS not found in project's settings.py file")
        self.labportalen_settings = settings.LABPORTALEN_SETTINGS

    def _validate_and_set_values(self) -> None:
        '''
        Validates if all the fields are present as fields_config.
        then sets the fields as instance fields
        '''
        for key, value in self.fields_config.items():
            field_value_in_settings = self.labportalen_settings.get(key)
            if value.get('required') and not field_value_in_settings:
                raise Exception(f"{key} is required but not given in LABPORTALEN_SETTINGS")
            elif not value.get('required') and not field_value_in_settings:
                setattr(self, key, value.get('default'))
            elif field_value_in_settings:
                if value.get('type') == Model:
                    field_value_in_settings = self._get_model(field_value_in_settings)
                setattr(self, key, field_value_in_settings)

    def _get_model(self, model_path_with_app_level: str) -> Model:
        '''
        Gets the Model class
        Parameters:
            model_path_with_app_level -> str: Model's path with the app level
                example: case.Case
        '''
        splitted_model_confg = model_path_with_app_level.split('.')
        model_name = splitted_model_confg.pop()
        app_level = '.'.join(splitted_model_confg)
        model = apps.get_model(app_label=app_level, model_name=model_name)
        return model

    def _get_models_for_list_of_model_types(self) -> None:
        '''
        Get models from a list of models
        '''
        for key, value in self.fields_config.items():
            if value.get('type') == BaseLabportalenService.TYPE_LIST_OF_MODELS:
                models_list = []
                for item in getattr(self, key):
                    model = self._get_model(item)
                    models_list.append(model)
                setattr(self, key, models_list)

    def is_valid(self) -> None:
        '''
        First setups the fields_config and then runs the validation
        '''
        self._setup_fields_config()
        self._validate_and_set_values()

    @abc.abstractmethod
    def _setup_fields_config(self) -> None:
        '''
        Setups the fields_config
        '''
        pass


class LabportalenService(BaseLabportalenService):
    def __init__(self) -> None:
        super().__init__()
        self.is_valid()
        self.REPORT_STATUS = {
            COMPLETED_REPLY_STATUS: LabportalenReport.SUCCESSFUL,
            PARTIAL_REPLY_STATUS: LabportalenReport.PARTIAL
        }

    def _setup_fields_config(self) -> None:
        '''
        Setups the fields_config
        '''
        self.fields_config['base_dir'] = {'required': True, 'type': str}
        self.fields_config['sftp_host'] = {'required': True, 'type': str}
        self.fields_config['sftp_username'] = {'required': True, 'type': str}
        self.fields_config['sftp_password'] = {'required': True, 'type': str}
        self.fields_config['sftp_file_prefix'] = {'required': True, 'type': str}
        self.fields_config['production_env_name'] = {'required': True, 'type': str}
        self.fields_config['current_env_name'] = {'required': True, 'type': str}

    def authenticate_to_sftp(self, max_retry: Optional[int] = 5, ) -> pysftp.Connection:

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        for item in range(max_retry):
            try:
                sftp = pysftp.Connection(
                    host=self.sftp_host,
                    username=self.sftp_username,
                    password=self.sftp_password,
                    cnopts=cnopts
                )
                print("Successfully connected to the sftp server")
                break
            except Exception as e:
                if item == (max_retry - 1):
                    raise Exception(
                        f"Can not connect to the SFTP server, Exception: {e}"
                    )
                sleep(10)
        return sftp

    def fetch_reports(self, requisition_id: Optional[str] = None) -> None:
        '''
        Fetches report from SFTP server
        Parameters:
            requisition_id -> str (Optional)
        Returns:
            None
        '''
        local_root_dir = os.path.join(self.base_dir, 'labportalen', 'sample_report')
        temp_path = local_root_dir + '/temp/'
        self._create_temp_dir_for_sftp_files(temp_path)
        sftp = self.authenticate_to_sftp()
        prefixed = [filename for filename in sftp.listdir() if filename.startswith(self.sftp_file_prefix)]
        for file_name in prefixed:
            print(file_name)
            local_file_name = temp_path + file_name
            try:
                sftp.get(file_name, localpath=local_file_name)
            except Exception as e:
                raise Exception(f"Couldn't get the file, {e}")
            with open(local_file_name, 'rb') as fp:
                data = fp.read()
                parsed_data = xmltodict.parse(data)
                self._save_parsed_xml_data(parsed_data, requisition_id)
            if self.current_env_name == self.production_env_name:
                try:
                    sftp.remove(file_name)
                except Exception as e:
                    raise Exception(f"can not remove file, {e}")
        sftp.close()
        print("SFTP Connection closed")
        self._delete_temp_dir_for_sftp_files(temp_path)

    def _create_temp_dir_for_sftp_files(self, temp_path: str) -> None:
        if not os.path.exists(temp_path):
            try:
                os.makedirs(temp_path)
            except OSError:
                raise Exception(
                    "Creation of the directory %s failed" % temp_path)

    def _get_unique_blood_test_results(self, old_result: list, new_result: list) -> list:
        '''
        new_result may contain duplicated blood marker which will be refined here to make it unique.
        Parameters:
            old_result -> list
            new_result -> list
        Returns:
            total_result: list
        '''
        new_gotten_analysis_codes = [code.get('analysis_code') for code in new_result]
        old_gotten_analysis_codes = [code.get('analysis_code') for code in old_result]
        new_gotten_analysis_codes.sort()
        old_gotten_analysis_codes.sort()
        print(f'len of old_test = {len(old_result)}')
        print(f'old_test = {old_gotten_analysis_codes}')
        print(f'len of new_test = {len(new_result)}')
        print(f'new_test = {new_gotten_analysis_codes}')
        for test in old_result:
            if test.get('analysis_code') not in new_gotten_analysis_codes:
                new_result.append(test)

        all_gotten_analysis_codes = [code.get('analysis_code') for code in new_result]
        all_gotten_analysis_codes.sort()
        print(f'all_test = {all_gotten_analysis_codes}')
        print(f'len of all_test = {len(new_result)}')
        return new_result

    def _save_report_data_to_db(self, requisition_id, test_results, reply_status):
        report_obj = LabportalenReport.objects.filter(rid=requisition_id).first()
        if report_obj:
            if report_obj.test_results:
                test_results = self._get_unique_blood_test_results(old_result=report_obj.test_results,
                                                                   new_result=test_results)
            report_obj.test_results = test_results
            if report_obj.status != LabportalenReport.SUCCESSFUL:
                report_obj.status = self.REPORT_STATUS.get(reply_status.upper(), LabportalenReport.PARTIAL)
            report_obj.save()
        else:
            report_obj = LabportalenReport.objects.create(
                rid=requisition_id,
                test_results=test_results,
                status=self.REPORT_STATUS.get(reply_status.upper(), LabportalenReport.PARTIAL)
            )

    @transaction.atomic
    def _save_parsed_xml_data(self, parsed_data: dict[Any, Any], requisition_id: Optional[str] = None) -> tuple:
        '''
        Parameters:
            parsed_data -> dict
            file_name -> str
            requisition_id -> str (Optional)
        Returns:
            requisition_id: str
            test_report: list
        '''
        requisition_info = parsed_data['InfoSolutionsMessage']['Requisition']
        if not requisition_id:
            requisition_id = requisition_info.get('@ExternalRequisitionID', None)
        reports = requisition_info['Reply']['Sample']['Analysis']
        reply_status = requisition_info['Reply'].get('@StatusCode')

        if type(reports) == list:
            test_results = {each.get('@TestMethodCode'): self._get_report_summary(each) for each in reports}.values()
            test_results = list(test_results)
        else:
            report_summary = self._get_report_summary(report=reports)
            test_results = [report_summary, ]

        self._save_report_data_to_db(requisition_id=requisition_id, test_results=test_results,
                                     reply_status=reply_status)
        return requisition_id, test_results

    def _get_report_summary(self, report):
        report_summary = {
            'analysis_name': report.get('@AnaName'),
            'analysis_code': report.get('@TestMethodCode'),
            'analysis_result': report.get('@Value'),
            'unit': report.get('@Unit'),
            'ref_text': report.get('@RefText'),
            'ref_mark': report.get('@RefMark'),
            'analysis_time': report.get('@AnalysisDateTime'),
            'priority_code': report.get('@PriorityCode')
        }
        return report_summary

    def _delete_temp_dir_for_sftp_files(self, temp_path):
        try:
            shutil.rmtree(temp_path)
        except OSError:
            raise OSError("Deletion of the directory %s failed" % temp_path)
