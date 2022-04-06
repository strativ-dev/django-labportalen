# Django import
from django.urls import path
from rest_framework import routers

# Self import
from labportalen.api.views import (
    CreateRemissApiView, 
    FetchReportForTestEnvApiView,
    LabportalenReportModelViewset,
)

router = routers.SimpleRouter()
router.register(
    'labportalen-reports',
    LabportalenReportModelViewset,
    'labportalen_report'
)

urlpatterns = [
    path('labportalen/create-remiss/', CreateRemissApiView.as_view(), name='create_remiss'),
    path('labportalen/fetch-report-for-test-env/', FetchReportForTestEnvApiView.as_view(), name='fetch_test_env_report'),
] + router.urls
