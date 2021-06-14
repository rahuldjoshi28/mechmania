# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
import json
import os

# Create your models here.
class College(models.Model):
    college = models.CharField(max_length=100,blank=False)
    def __str__(self):
        return self.college+""

class Subject(models.Model):
    subject = models.CharField(max_length=50,blank=False)
    def __str__(self):
        return self.subject+""

class Papers(models.Model):
    year = models.CharField(max_length=10,blank=False)
    term = models.CharField(max_length=10,default='')
    description = models.CharField(max_length=500)
    paper = models.FileField(upload_to="static/papersDir/", null=False, blank=False);
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    def as_json(self):
        fileName = str(self.subject.subject)
        if (self.college):
            fileName = fileName + '-' + str(self.college.college)
        fileName = fileName + '-' + self.year
        return dict(
            paper_id = self.id,
            paper_name = fileName
        )

    def filename(self):
        return os.path.basename(self.file.name)

class PapersSearchFields(admin.ModelAdmin):
    search_fields = ['year','description','subject','college','paper','term']
