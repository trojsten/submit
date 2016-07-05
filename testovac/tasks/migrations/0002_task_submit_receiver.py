# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-08 15:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0001_initial'),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='submit_receiver',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='submit.SubmitReceiver'),
            preserve_default=False,
        ),
    ]
