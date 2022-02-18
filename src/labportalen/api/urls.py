# Django import
from django.urls import path
# Self import
from labportalen.api.views import (
    CreateRemissApiView, 
    FetchReportForTestEnvApiView)


urlpatterns = [
    path('labportalen/create-remiss/', CreateRemissApiView.as_view(), name='create_remiss'),
    path('labportalen/fetch-report-for-test-env/', FetchReportForTestEnvApiView.as_view(), name='fetch_test_env_report'),
]
