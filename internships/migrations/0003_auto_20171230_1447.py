# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-30 09:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0002_industry_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internship',
            name='stipend',
            field=models.IntegerField(),
        ),
    ]
