# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-23 17:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_profile_resume'),
        ('internships', '0008_auto_20180103_0058'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoneIV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='IVRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='PrevIV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IV', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internships.DoneIV')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='RequestNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('IVRequest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internships.IVRequest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='UpcomingIV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateConf', models.DateField()),
                ('letter', models.FileField(blank=True, upload_to='')),
                ('IVRequest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internships.IVRequest')),
            ],
        ),
        migrations.AddField(
            model_name='industrialvisit',
            name='minimumCount',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='industrialvisit',
            name='isavailable',
            field=models.CharField(choices=[('a', 'available'), ('na', 'not available')], default='na', max_length=2),
        ),
        migrations.AddField(
            model_name='ivrequest',
            name='IV',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internships.IndustrialVisit'),
        ),
        migrations.AddField(
            model_name='ivrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.Profile'),
        ),
        migrations.AddField(
            model_name='group',
            name='IVRequest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internships.IVRequest'),
        ),
        migrations.AddField(
            model_name='group',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.Profile'),
        ),
        migrations.AddField(
            model_name='doneiv',
            name='IV',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internships.IndustrialVisit'),
        ),
    ]
