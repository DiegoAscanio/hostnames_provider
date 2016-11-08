'''
        @file serializers.py
        @lastmod 8/11/2016
'''

from rest_framework import serializers
from .models import Host
from django.db import models

# Serializer da Classe Host
class HostSerializer(serializers.ModelSerializer):
    '''
    Classe Serializadora de Host: Indica a Classe que servira de modelo e seus determinados campos 
    '''
    class Meta:
        model = Host
        fields = ('hostname','mac_address','ip_address')
