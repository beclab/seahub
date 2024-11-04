DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'seahub',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
FILE_SERVER_ROOT = '/seafhttp'

import os
PROJECT_ROOT = '/root/dev/source-code/seahub'
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'frontend/',
        'STATS_FILE': os.path.join(PROJECT_ROOT,
                                   'frontend/webpack-stats.dev.json'),
    }
}
DEBUG = True

CSRF_TRUSTED_ORIGINS = ['https://seafile.liuy102.snowinning.com']

ENABLE_ONLYOFFICE = True
ONLYOFFICE_APIJS_URL = 'http://onlyoffice.onlyoffice-wangrongxiang2:80/web-apps/apps/api/documents/api.js' # 'http://seafile.example.com:6233/web-apps/apps/api/documents/api.js'
ONLYOFFICE_FILE_EXTENSION = ('doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'odt', 'fodt', 'odp', 'fodp', 'ods', 'fods', 'csv', 'ppsx', 'pps')
ONLYOFFICE_JWT_SECRET = 'N21HeGlxQlQ='
