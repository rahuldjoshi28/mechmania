from django.db import models
from internships.models import industry
from datetime import date
from Accounts.models import Profile
from django.utils import timezone

class Project(models.Model):
    company=models.ForeignKey(industry,on_delete=models.CASCADE,blank=False)
    description=models.TextField(max_length=10000)
    number=models.IntegerField(default=0)
    type=models.CharField(max_length=20)
    AVAILABLE_CHOICES = (('yes', 'available'), ('no', 'not available'))
    isavailable = models.CharField(choices=AVAILABLE_CHOICES, max_length=3, default='yes')
    minimumCnt=models.IntegerField(default=3)
    def __str__(self):
        return str(self.company.__str__)+" "+str(self.id)
class ProjectRequest(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE,blank=False)
    project=models.ForeignKey(Project,on_delete=models.CASCADE,blank=False)
    date=models.DateField(default=date.today)
    def __str__(self):
        return str(self.user.__str__)+" "+str(self.id)
class ProjectGroup(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE,blank=False)
    ProjectRequest=models.ForeignKey(ProjectRequest,on_delete=models.CASCADE,blank=False)
    def __str__(self):
        return str(self.user.__str__)+" "+str(self.id)
class ProjectNotice(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE,blank=False)
    ProjectRequest=models.ForeignKey(ProjectRequest,on_delete=models.CASCADE,blank=False)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    def __str__(self):
        return str(self.user.__str__)+" "+str(self.id)
class AcceptedGroup(models.Model):
    ProjectRequest=models.ForeignKey(ProjectRequest,on_delete=models.CASCADE,blank=False)
    dateConf=models.DateField(blank=False)
    letter=models.FileField(blank=True)
    def __str__(self):
        return str(self.user.__str__)+" "+str(self.id)