# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-01 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0004_profile_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='static/Resumes/'),
        ),
    ]
