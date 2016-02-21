from django.db import models

# Create your models here.

class Host(models.Model):
    hostname = models.CharField(max_length=15)
    mac_address = models.CharField(max_length=17)
    ip_address = models.TextField(unique=True)
    def __str__(self):
        return self.hostname+'|'+self.mac_address+'|'+self.ip_address
