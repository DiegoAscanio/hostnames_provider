# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostnames', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='ip_address',
            field=models.CharField(unique=True, max_length=15),
        ),
    ]
