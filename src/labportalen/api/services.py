# Python import
from typing import Any

# Django import
from django.db import transaction
from django.db.models import Model
from rest_framework.exceptions import (
    NotAcceptable, 
    NotFound, 
    ParseError,
)

# Self import
from labportalen.soap_service.services import SoapServices
from labportalen.models import HealthCheckType
from labportalen.api.serializers import (
    AnalysisSerializerForSoapService,
    FetchReportForTestEnvSerializer,
)
from labportalen.services import (
    BaseLabportalenService, 
    LabportalenService,
)


class LabportalenApiServices(BaseLabportalenService):

    def __init__(self) -> None:
        super().__init__()
        self.is_valid()
        self._get_models_for_list_of_model_types()

    @transaction.atomic
    def create_remiss(self, data: dict[Any, Any], user: Model) -> dict:
        '''
        Creates E-Remiss in labportal
        Parameters:
            data -> dict
            rid_mapping_models -> list
            user -> Model : user model
        Returns:
            response -> dict    
        '''
        case = self.case_model.objects.filter(uid=data.get('case')).first()
        if not case:
            raise NotFound('No case found by the given case id')
        analysis_list, lab_code = self.get_analyses_list_and_lab_code(case.health_check_type_code)
        soap_service = SoapServices(
            self.soap_service_wsdl_url, 
            self.customer_code,
            self.requnitcode,
            self.company_name,
            self.contact_person,
            self.user_guid,
            lab_code,
            self.department_id,
            self.reservenumber_prefix,
            analysis_list)

        response = soap_service.send_referral_with_object(patient_data=data)
        requisation_id = response.get('Rid')
        if not requisation_id:
            error_description = response.get('Description')
            raise NotAcceptable(f'No Rid returned from Labportalen. {error_description}')

        if self.rid_mapping_models:
            for model_name in self.rid_mapping_models:
                model_name.objects.get_or_create(case=case, rid=requisation_id, created_by=user)

        if hasattr(case, 'allow_remiss_creation'):
            case.allow_remiss_creation = False
        if hasattr(case, 'is_blood_report_received'):
            case.is_blood_report_received = False
        if hasattr(case, 'last_blood_report_received_at'):
            case.last_blood_report_received_at = None
        case.save()
        return response
    
    def get_analyses_list_and_lab_code(self, health_check_type_code: str) -> tuple:
        '''
        Returns analises corresponding to the health_check_type
        Parameters:
            health_check_type_code -> str
        Returns:
            analyses_list_and_lab_code -> tuple
        '''
        health_check_type = HealthCheckType.objects.filter(health_check_type_code=health_check_type_code).first()
        if not health_check_type:
            raise NotFound('No health check found with code name {health_check_type_code}')
        analyses = AnalysisSerializerForSoapService(health_check_type.analyses.all(), many=True).data
        if len(analyses) == 0:
            raise NotAcceptable('No analysis found with this health check type')
        return analyses, health_check_type.conduction_lab.lab_code

    def fetch_test_env_report(self, data: dict) -> bool:
        if self.current_env_name == self.production_env_name:
            raise NotAcceptable('This action is not acceptable in production environment')
        
        FetchReportForTestEnvSerializer(data=data).is_valid(raise_exception=True)
        
        try:
            LabportalenService().fetch_reports(requisition_id=data['rid'])
        except Exception as e:
            raise ParseError(f'Encountered error during fetching: {e}')
        return True
    
    def _setup_fields_config(self) -> None:
        '''
        Setups the field_configs
        '''
        self.fields_config['production_env_name'] = {'required': True, 'type': str}
        self.fields_config['current_env_name'] = {'required': True, 'type': str}
        self.fields_config['rid_mapping_models'] = {'required': False, 'default': None, 'type': BaseLabportalenService.TYPE_LIST_OF_MODELS}
        self.fields_config['soap_service_wsdl_url'] = {'required': True, 'type': str}
        self.fields_config['customer_code'] = {'required': True, 'type': str}
        self.fields_config['requnitcode'] = {'required': True, 'type': str}
        self.fields_config['company_name'] = {'required': True, 'type': str}
        self.fields_config['contact_person'] = {'required': True, 'type': str}
        self.fields_config['user_guid'] = {'required': False, 'default': '', 'type': str}
        self.fields_config['department_id'] = {'required': True, 'type': str}
        self.fields_config['reservenumber_prefix'] = {'required': False, 'default': '', 'type': str}