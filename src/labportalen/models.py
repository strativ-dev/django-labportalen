# Python import

# Django import
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Self import


class Lab(models.Model):
    lab_name = models.CharField(
        max_length=250, 
        verbose_name=_('Lab name'), 
        db_column='lab_name',
    )
    lab_code = models.CharField(
        max_length=250, 
        verbose_name=_('Lab code'), 
        db_column='lab_code',
        unique=True,
    )

    def __str__(self) -> str:
        return f"Lab name: {self.lab_name}, Lab code: {self.lab_code}"
    
    class Meta:
        db_table = 'Lab'
        verbose_name_plural = 'Labs'

class Analysis(models.Model):
    analysis_name = models.CharField(
        max_length=250, 
        verbose_name=_('Analysis name'), 
        db_column='analysis_name'
    )
    analysis_code = models.CharField(
        max_length=250, 
        verbose_name=_('Analysis code'), 
        db_column='analysis_code', 
        unique=True
    )

    def __str__(self) -> str:
        return f"Analysis name: {self.analysis_name}, Analysis code: {self.analysis_code}"

    class Meta:
        db_table = 'Analysis'
        verbose_name_plural = 'Analyses'

class HealthCheckType(models.Model):
    health_check_type_name = models.CharField(
        max_length=250, 
        verbose_name=_('Health check type name'), 
        db_column='health_check_type'
    )
    health_check_type_code = models.CharField(
        max_length=250, 
        verbose_name=_('Health check type code'), 
        db_column='health_check_type_code', 
        unique=True
    )
    analyses = models.ManyToManyField(
        'labportalen.Analysis', 
        verbose_name=_('Analyses'), 
        db_column='analyses', 
        related_name='health_check_type_analyses'
    )
    conduction_lab = models.ForeignKey(
        'labportalen.Lab', 
        verbose_name=_('Conduction lab'), 
        db_column='conduction_lab', 
        related_name='lab_health_check_type', 
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"Health check name: {self.health_check_type_name}"
    
    class Meta:
        db_table = 'HealthCheckType'
        verbose_name_plural = 'Health check types'

class LabportalenReport(models.Model):
    PENDING = 'pending'
    SUCCESSFUL = 'successful'
    PARTIAL = 'partial'
    FAILED = 'failed'
    BLOOD_TEST_STATUS_CHOICES = [
        (PENDING, _('pending')),
        (SUCCESSFUL, _('successful')),
        (PARTIAL, _('partial')),
        (FAILED, _('failed'))
    ]
    rid = models.CharField(
        max_length=250, 
        verbose_name=_('Rid'), 
        db_column='rid', 
        unique=True
    )
    test_results = models.JSONField(
        verbose_name=_('Test results'), 
        db_column='test_result', 
        null=True, 
        blank=True
    )
    status = models.CharField(
        max_length=30, 
        choices=BLOOD_TEST_STATUS_CHOICES, 
        default=PENDING, 
        verbose_name=_('Status'), 
        db_column='status'
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created at'), 
        db_column='created_at', 
        auto_now_add=True, 
        editable=False
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated at'), 
        db_column='updated_at', 
        auto_now=True, 
        null=True,
        blank=True
    )
    
    def __str__(self):
        return self.rid
    
    class Meta:
        db_table = 'LabportalenReport'
        verbose_name_plural = 'Labportalen reports'