# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-10 08:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20160509_1605'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='submit_receiver',
            new_name='submit_receivers',
        ),
    ]