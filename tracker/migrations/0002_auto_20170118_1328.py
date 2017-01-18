# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='device_ip',
            field=models.IPAddressField(blank=True),
        ),
        migrations.AlterField(
            model_name='mail',
            name='last_read',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 18, 13, 28, 2, 788756, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
    ]
