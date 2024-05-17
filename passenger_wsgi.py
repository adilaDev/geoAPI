import sys
sys.path.insert(0, "/home/u8378009/public_html/geofence-api.asiaresearchinstitute.com/geoAPI")
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'geoAPI.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()