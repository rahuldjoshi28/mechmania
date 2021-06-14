# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Quotes(models.Model):
    quote = models.TextField(max_length=500, blank=True, null=True)
    quotedBy = models.TextField(max_length=200, blank=True, null=True)
