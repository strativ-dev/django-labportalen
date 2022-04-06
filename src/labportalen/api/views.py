# Python import

# Django import
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated

# Self import
from labportalen.models import LabportalenReport
from labportalen.api.serializers import (
    CreateRemissSerializer,
    LabportalenReportSerializer
)
from labportalen.api.services import LabportalenApiServices

class CreateRemissApiView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        data = request.data
        CreateRemissSerializer(data=data).is_valid(raise_exception=True)
        response = LabportalenApiServices().create_remiss(data, request.user)
        return Response(response, status=HTTP_200_OK)
    

class FetchReportForTestEnvApiView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        data = request.data
        fetched = LabportalenApiServices().fetch_test_env_report(data)
        return Response({'Fetched': fetched}, status=HTTP_200_OK)

class LabportalenReportModelViewset(ModelViewSet):
    model = LabportalenReport
    serializer_class = LabportalenReportSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'retrieve']
