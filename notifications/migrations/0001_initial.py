# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-23 18:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Accounts', '0005_profile_resume'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=1000)),
                ('message', models.CharField(max_length=5000)),
                ('link', models.CharField(blank=True, max_length=100)),
                ('is_read', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.Profile')),
            ],
        ),
    ]
