python manage.py shell
from hostnames.models import Host
from hostnames.serializers import HostSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

