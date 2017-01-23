# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20170118_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='last_read',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
