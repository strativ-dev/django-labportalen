# Python import

# Django import
from rest_framework import serializers

# Self import
from labportalen.models import Analysis


class CreateRemissSerializer(serializers.Serializer):
    '''
    Determines the fields to take input through endpoints for remiss creation
    '''
    case = serializers.CharField(required=True)
    patient_personnumber = serializers.CharField(required=True)
    patient_first_name = serializers.CharField(required=False)
    patient_sur_name = serializers.CharField(required=False)
    patient_phone_number = serializers.CharField(required=False)
    patient_gender = serializers.CharField(required=False)

class FetchReportForTestEnvSerializer(serializers.Serializer):
    '''
    Determines the fields to take input through endpoints for
    fetching test env report fetching
    '''
    rid = serializers.CharField(required=True)

class AnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Analysis
        fields = ['analysis_name', 'analysis_code']


class AnalysisSerializerForSoapService(serializers.ModelSerializer):
    AnalysisName = serializers.CharField(source='analysis_name')
    AnalysisCode = serializers.CharField(source='analysis_code')
    class Meta:
        model = Analysis
        fields = ['AnalysisName', 'AnalysisCode']
