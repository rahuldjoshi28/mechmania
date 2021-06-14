# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-16 20:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(max_length=10)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='M', max_length=1)),
                ('about', models.TextField(blank=True, max_length=500)),
                ('address', models.TextField(blank=True, max_length=500)),
                ('college_name', models.CharField(blank=True, max_length=100)),
                ('branch', models.CharField(blank=True, max_length=100)),
                ('is_applied_to_industrialVisit', models.IntegerField(default=0)),
                ('is_applied_to_internship', models.IntegerField(default=0)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='static/profile_pics/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]