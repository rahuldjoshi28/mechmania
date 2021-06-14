# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    mobile_number = models.CharField(max_length=10, blank=False)
    birth_date=models.DateField(null=True, auto_now=False, auto_now_add=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', blank=False)
    about = models.TextField(max_length=500, blank=True)
    address = models.TextField(max_length=500, blank=True)
    college_name = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    is_applied_to_industrialVisit = models.IntegerField(default=0)
    is_applied_to_internship = models.IntegerField(default=0)
    is_admin = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='static/profile_pics/', null=True, blank=True)
    resume = models.FileField(upload_to="static/Resumes/", null=True, blank=True);
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
