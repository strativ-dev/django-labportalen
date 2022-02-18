from django.contrib import admin

# Self imports
from labportalen.models import Lab, Analysis, HealthCheckType

# Register your models here.
class LabModelAdmin(admin.ModelAdmin):
    list_display = ['lab_name', 'lab_code']
    search_fields = ['lab_name']

admin.site.register(Lab, LabModelAdmin)

class AnalysisModelAdmin(admin.ModelAdmin):
    list_display = ['analysis_name', 'analysis_code']
    search_fields = ['analysis_name', 'analysis_code']

admin.site.register(Analysis, AnalysisModelAdmin)

class HealthCheckTypeModelAdmin(admin.ModelAdmin):
    list_display = ['health_check_type_name', 'health_check_type_code', 'conduction_lab']
    search_fields = ['health_check_type_name', 'health_check_type_code', 'conduction_lab']

admin.site.register(HealthCheckType, HealthCheckTypeModelAdmin)