# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
from . import base

if base.DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'root',
            'NAME': 'todo',
            'PASSWORD': 'root',
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                # Tell MySQLdb to connect with 'utf8mb4' character set
                'charset': 'utf8mb4',
                'init_command': 'SET innodb_strict_mode=1',
                # 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
            # Tell Django to build the test database with the 'utf8mb4' character set
            'TEST': {
                'CHARSET': 'utf8mb4',
                'COLLATION': 'utf8mb4_unicode_ci',
            }
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'svaghari$doctornotes',
            'USER': 'svaghari',
            'PASSWORD': "yDLV5bhVJrzpbFtA",
            'HOST': 'svaghari.mysql.pythonanywhere-services.com',
            'OPTIONS': {
                # Tell MySQLdb to connect with 'utf8mb4' character set
                'charset': 'utf8mb4',
                'init_command': 'SET innodb_strict_mode=1',
            },
            # Tell Django to build the test database with the 'utf8mb4' character set
            'TEST': {
                'CHARSET': 'utf8mb4',
                'COLLATION': 'utf8mb4_unicode_ci',
            }
        }
    }


