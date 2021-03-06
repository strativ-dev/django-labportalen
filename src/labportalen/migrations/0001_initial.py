# Generated by Django 3.2.9 on 2022-02-18 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analysis_name', models.CharField(db_column='analysis_name', max_length=250, verbose_name='Analysis name')),
                ('analysis_code', models.CharField(db_column='analysis_code', max_length=250, unique=True, verbose_name='Analysis code')),
            ],
            options={
                'verbose_name_plural': 'Analyses',
                'db_table': 'Analysis',
            },
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_name', models.CharField(db_column='lab_name', max_length=250, verbose_name='Lab name')),
                ('lab_code', models.CharField(db_column='lab_code', max_length=250, verbose_name='Lab code')),
            ],
            options={
                'verbose_name_plural': 'Labs',
                'db_table': 'Lab',
            },
        ),
        migrations.CreateModel(
            name='LabportalenReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rid', models.CharField(db_column='rid', max_length=250, unique=True, verbose_name='Rid')),
                ('test_results', models.JSONField(blank=True, db_column='test_result', null=True, verbose_name='Test results')),
                ('status', models.CharField(choices=[('pending', 'pending'), ('successful', 'successful'), ('partial', 'partial'), ('failed', 'failed')], db_column='status', default='pending', max_length=30, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='updated_at', null=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name_plural': 'Labportalen reports',
                'db_table': 'LabportalenReport',
            },
        ),
        migrations.CreateModel(
            name='HealthCheckType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('health_check_type_name', models.CharField(db_column='health_check_type', max_length=250, verbose_name='Health check type name')),
                ('health_check_type_code', models.CharField(db_column='health_check_type_code', max_length=250, unique=True, verbose_name='Health check type code')),
                ('analyses', models.ManyToManyField(db_column='analyses', related_name='health_check_type_analyses', to='labportalen.Analysis', verbose_name='Analyses')),
                ('conduction_lab', models.ForeignKey(db_column='conduction_lab', on_delete=django.db.models.deletion.CASCADE, related_name='lab_health_check_type', to='labportalen.lab', verbose_name='Conduction lab')),
            ],
            options={
                'verbose_name_plural': 'Health check types',
                'db_table': 'HealthCheckType',
            },
        ),
    ]
