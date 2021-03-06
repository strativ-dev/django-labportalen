==================
django-labportalen
==================

``django-labportalen`` is a Django app to communicate with swedish Labportalen service. Suitable till eRemiss version 3.1.0.


Features
--------
- Configure several analyses for different health checks.
- Create remiss for a patient against a health check type.
- Fetch analyses reports from SFTP server.


Quick start
-----------
1. Install ``django-labportalen`` like this::

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
    'base_dir': BASE_DIR,                        ## -> project's base directory: (required for all services)
    'sftp_host': env('SFTP_HOSTNAME'),           ## -> SFTP server where XML reports will be uploaded: (required to use SFTP service)
    'sftp_username': env('SFTP_USERNAME'),       ## -> SFTP server where XML reports will be uploaded: (required to use SFTP service)
    'sftp_password': env('SFTP_PASSWORD'),       ## -> SFTP server where XML reports will be uploaded: (required to use SFTP service)
    'sftp_file_prefix': env('SFTP_FILE_PREFIX'), ## -> SFTP server where XML reports will be uploaded: (required to use SFTP service)
    'production_env_name': 'PRODUCTION',         ## -> production server name: (required for all services)
    'current_env_name': 'DEV',                   ## -> current server name where this code base is going to be executed: (required for all services)
    'soap_service_wsdl_url': env('SERVICE_URL'), ## -> WSDL url where remiss creation request will be posted: (required to use remiss creation service)
    'customer_code': env('CUSTOMER_CODE'),       ## -> customer code provided by labportalen: (required to use remiss creation service)
    'requnitcode': env('REQUNITCODE'),           ## -> requnitcode provided by labportalen: (required to use remiss creation service)
    'company_name': env('COMPANY_NAME'),         ## -> company name provided by labportalen: (required to use remiss creation service)
    'contact_person': env('CONTACT_PERSON'),     ## -> contact person name provided by labportalen: (required to use remiss creation service)
    'user_guid': os.environ.get('USER_GUID',''), ## -> user guid provided by labportalen: (optional)
    'department_id': env('DEPARTMENTID'),        ## -> department id provided by labportalen: (required to use remiss creation service)
    'reservenumber_prefix': env('RESERVENUMBER_PREFIX'),               ## -> reservenumber prefix provided by labportalen: (optional)
    'case_model': 'case.Case',                                         ## -> case model against which remisses will be created: (required)
    'rid_mapping_models': ['case.CaseRid', 'patient_tests.BloodTest'], ## -> if you want to map rids against cases to trace which rid belongs to which case.         
    }                                                                  ##    should be many to one relation: (optional)
    ## It is recommended to take the credentials from a .env file.

6. Start the development server and visit http://127.0.0.1:8000/labportalen/api/
   to see available labportalen end-points.


Contributing
------------
If you face any issues with project, please create and submit an issue,
detailing the problem and providing examples to reproduce the problem.

If you wish to contribute to the project via enhancements, please submit an
issue outlining how your suggested changes improves the project and the scope of
the change.
