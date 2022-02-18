# Python import
import datetime
from typing import Any
from zeep import helpers
import json

# Django import


# Self import
from labportalen.soap_service.client import WsdlClient


class SoapServices(object):
    def __init__(self, 
        service_url: str,
        customer_code: str,
        requnitcode: str,
        company_name: str,
        contact_person: str,
        user_guid: str,
        laboratory_code: str,
        department_id: str,
        reservenumber_prefix: str,
        analysis_list: list
        ):
        super().__init__()
        self.customer_code = customer_code
        self.requnitcode = requnitcode
        self.company_name = company_name
        self.contact_person = contact_person
        self.user_guid = user_guid
        self.laboratory_code = laboratory_code
        self.department_id = department_id
        self.reservenumber_prefix = reservenumber_prefix
        self.analysis_list = analysis_list
        self.client = WsdlClient(wsdl_url=service_url).get_client()

    @staticmethod
    def label_gender(personnumber: int) -> str:
        '''
        Takes personnumber as input and returns person's gender as number based on the last two digit.
        Parameters:
            personnumber -> int
        Returns:
            label_gender -> str    
        '''
        if int(personnumber[-2]) % 2 == 0:
            return "77"
        else:
            return "75"

    @staticmethod
    def label_gender_from_patient_gender(gender: str) -> str:
        '''
        Takes gender as argument and returns gender as number
        Parameters:
            gender -> str
        Returns:
            label_gender -> str
        '''
        if gender == 'kvinna':
            return "77"
        else:
            return "75"

    def send_referral_with_object(self, patient_data: dict[Any, Any]) -> dict:
        '''
        Parameters:
            patient_data -> dict
            eremiss_prod -> bool
        Returns:
            response -> dict : Response from Labportalen    
        '''
        patient_data["patient_personnumber"] = str(
            patient_data["patient_personnumber"])
        if patient_data["patient_personnumber"].startswith(self.reservenumber_prefix):
            patient_gender = self.label_gender_from_patient_gender(
                gender=patient_data["patient_gender"])
            is_reserved_patient_id = True
        else:
            patient_gender = self.label_gender(
                patient_data["patient_personnumber"])
            is_reserved_patient_id = False
        # Payload
        referral_data = {
            "CustomerCode": self.customer_code,
            "ExternalRequisitionId": "",
            "mpatient": {
                "PatientFirstName": patient_data.get('patient_first_name', ""),
                'PatientSurName': patient_data.get('patient_sur_name', ""),
                'PatientAddress': "",
                'PatientPostalCode': "",
                'PatientPostalAddress': "",
                'PatientPhoneNumber': patient_data.get('patient_phone_number', ""),
                'PatientCellPhoneNumber': "",
                'PatientID': patient_data.get('patient_personnumber', ""),
                'PatientSex': patient_gender,
                'IsReservePatientID': is_reserved_patient_id

            },
            "mrequnit": {
                "Code": self.requnitcode,
                "Name": self.company_name,
                "ContactPerson": self.contact_person,
                'UserGuid': self.user_guid
            },
            "mpayunit": {
                "Code": self.requnitcode,
                "Name": self.company_name
            },
            "LaboratoryCode": self.laboratory_code,
            "AnalysisList": {
                "Analysis": self.analysis_list
            },
            "QuestionList": None,
            "ReferralComment": patient_data["referral_comment"] if patient_data.get("referral_comment") else "",
            "ReferralType": "save",
            "OptionalParams": {
                "FormID": 0,
                "Acute": "",
                "TestDateChanged": "",
                "DepartmentID": self.department_id,
                "SampleIDs": ["", ],
                "TestDate": datetime.datetime.now(),
                "ByPassKey": "",
                "LID": "",
                "CopyUnit1": "",
                "CopyUnit2": "",
                "SamplerComment": "",
                "ReferralStatus": "78",
                "SendAsSampled": False,
                "RequisitionType": 1
            }
        }
        response = self.client.service.SendReferralWithObject(**referral_data)
        input_dict = helpers.serialize_object(response)
        output_dict = json.loads(json.dumps(input_dict))
        return output_dict