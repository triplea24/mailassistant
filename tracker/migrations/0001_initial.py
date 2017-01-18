# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('url', models.TextField(blank=True)),
                ('device_ip', models.IPAddressField(default=b'127.0.0.1')),
                ('device_browser', models.TextField(blank=True)),
                ('device_browser_family', models.TextField(blank=True)),
                ('device_browser_version_string', models.TextField(blank=True)),
                ('device_os', models.TextField(blank=True)),
                ('device_os_family', models.TextField(blank=True)),
                ('device_os_version_string', models.TextField(blank=True)),
                ('device_type', models.TextField(blank=True)),
                ('device_type_family', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(null=True)),
                ('subject', models.TextField()),
                ('last_read', models.DateTimeField(null=True)),
                ('count', models.IntegerField(default=0)),
                ('track_key', models.CharField(unique=True, max_length=36, blank=True)),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Receiver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('type_of_receiption', models.CharField(default=b'T', max_length=1, choices=[(b'T', b'TO'), (b'C', b'CC'), (b'B', b'BCC')])),
                ('mail', models.ForeignKey(to='tracker.Mail')),
            ],
        ),
        migrations.AddField(
            model_name='log',
            name='mail',
            field=models.ForeignKey(to='tracker.Mail'),
        ),
    ]
