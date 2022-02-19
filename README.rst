==================
django-labportalen
==================

``django-labportalen`` is a Django app to communicate with swedish Labportalen service. Suitable with eRemiss version 3.1.0.

Features
--------
- Create remiss for a patient against a case.
- Fetch analyses reports from SFTP server.


Detailed documentation is in the "docs" directory.

Quick start
-----------
1. Install ``django-labportalen`` like this::

    pip install --upgrade pip
    pip install django-labportalen

2. Add "labportalen" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'labportalen',
    ]

3. Include the labportalen URLconf in your project urls.py like this::

    path('labportalen/', include('labportalen.urls')),

4. Run ``python manage.py migrate`` to create the labportalen models.

5. Configure LABPORTALEN_SETTINGS with required values in your project's ``settings.py``::

    LABPORTALEN_SETTINGS = {
    'base_dir': BASE_DIR,                        ## required for all services
    'sftp_host': env('SFTP_HOSTNAME'),           ## required to user SFTP service
    'sftp_username': env('SFTP_USERNAME'),       ## required to user SFTP service
    'sftp_password': env('SFTP_PASSWORD'),       ## required to user SFTP service
    'sftp_file_prefix': env('SFTP_FILE_PREFIX'), ## required to user SFTP service
    'production_env_name': 'PRODUCTION',         ## required for all services
    'current_env_name': 'DEV',                   ## required for all services
    'soap_service_wsdl_url': env('SERVICE_URL'), ## required to use remiss creation service
    'customer_code': env('CUSTOMER_CODE'),       ## required to use remiss creation service
    'requnitcode': env('REQUNITCODE'),           ## required to use remiss creation service
    'company_name': env('COMPANY_NAME'),         ## required to use remiss creation service
    'contact_person': env('CONTACT_PERSON'),     ## required to use remiss creation service
    'user_guid': os.environ.get('USER_GUID',''), ## optional
    'department_id': env('DEPARTMENTID'),        ## required to use remiss creation service
    'reservenumber_prefix': env('RESERVENUMBER_PREFIX'),               ## optional
    'case_model': 'case.Case',                                         ## required
    'rid_mapping_models': ['case.CaseRid', 'patient_tests.BloodTest'], ## optional
    }

6. Start the development server and visit http://127.0.0.1:8000/labportalen/api/
   to see available labportalen end-points.