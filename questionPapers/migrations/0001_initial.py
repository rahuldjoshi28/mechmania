# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-21 18:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='paper',
            name='Subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionPapers.Subject'),
        ),
        migrations.AddField(
            model_name='paper',
            name='college',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionPapers.College'),
        ),
    ]
