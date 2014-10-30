import os
import sys

path = '/var/www/doc_maker'
if path not in sys.path:
    sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'doc_maker.settings'

import django.core.handlers.wsgi
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

