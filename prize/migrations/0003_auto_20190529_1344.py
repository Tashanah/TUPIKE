# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-29 13:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0002_auto_20190529_1306'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ratings',
            old_name='usabilty',
            new_name='usability',
        ),
    ]
