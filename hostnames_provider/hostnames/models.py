'''
        @file models.py
        @lastmod 9/11/2016
'''

# Importacoes
from django.db import models
import django
from django import forms

# Area de criacao de classes

# Classe do Host
class Host(models.Model):
    '''
    Classe de Host: Armazena um hostname, e seus Enderecos Mac e IP
    '''
    hostname = models.CharField(max_length=15)
    mac_address = models.CharField(max_length=17)
    ip_address = models.CharField(primary_key=True, unique=True, max_length=15)
    def __str__(self):
        return self.hostname+'|'+self.mac_address+'|'+self.ip_address






