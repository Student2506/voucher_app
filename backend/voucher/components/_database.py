import os

POSTGRES_DB_PORT = 5432
MSSQL_DB_PORT = 1433

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST', '127.0.0.1'),
        'PORT': os.environ.get('POSTGRES_PORT', POSTGRES_DB_PORT),
        'OPTIONS': {
            'options': '-c search_path=voucher_app,public',
        },
    },
    'vista': {
        'ENGINE': 'mssql',
        'NAME': os.environ.get('MSSQL_DB'),
        'USER': os.environ.get('MSSQL_USER'),
        'PASSWORD': os.environ.get('MSSQL_PASSWORD'),
        'HOST': os.environ.get('MSSQL_HOST'),
        'PORT': os.environ.get('MSSQL_PORT', MSSQL_DB_PORT),
        'Trusted_Connection': 'no',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'unicode_results': 'yes',
            'extra_params': 'TrustServerCertificate=yes',
        },
    },
}
