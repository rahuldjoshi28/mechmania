from django.db import models
from Accounts.models import Profile
from django.utils import timezone
from datetime import date

class industry(models.Model):
    name=models.CharField(max_length=50,blank=False)
    logo=models.ImageField(upload_to='static/CompanyLogos/',blank=True)
    description=models.TextField(max_length=10000)
    mail=models.CharField(max_length=50,blank=True,null=True)
    address=models.CharField(max_length=500,null=False)
    website=models.CharField(max_length=500)
    latitude=models.CharField(max_length=50)
    longitude=models.CharField(max_length=50)
    city=models.CharField(max_length=50,default='india')
    def __str__(self):
        return str(self.name)
    def filename(self):
        return str(self.logo.name)

class internship(models.Model):
    company=models.ForeignKey(industry,on_delete=models.CASCADE,blank=False)
    stipend=models.IntegerField()
    startdate=models.DateField()
    enddate=models.DateField()
    description=models.TextField(max_length=10000)
    qualification=models.TextField(max_length=10000)
    type=models.CharField(max_length=20)
    def __str__(self):
        return str(self.company.__str__)+" "+str(self.id)

class InternshipRequest(models.Model):
    user = models.ForeignKey(Profile, on_delete = models.CASCADE, blank=False)
    internship = models.ForeignKey(internship, on_delete=models.CASCADE, blank=False)
    def __str__(self):
        return self.user.user.username + " " + self.internship.company.name

class ConfirmedInternships(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False)
    internship = models.ForeignKey(internship, on_delete=models.CASCADE, blank=False)

# Nitin
class IndustrialVisit(models.Model):
    type = models.CharField(max_length=20, blank=False)
    duration = models.IntegerField()
    description = models.TextField(max_length=100)
    company = models.ForeignKey(industry, on_delete=models.CASCADE, blank=False)
    AVAILABLE_CHOICES = (('a', 'available'), ('na', 'not available'))
    ratings = models.FloatField()
    isavailable = models.CharField(choices=AVAILABLE_CHOICES, max_length=2, default='na')
    minimumCount = models.IntegerField(default=10)

    def __str__(self):
        return str(self.company.__str__) + " " + str(self.id)


class IVRequest(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False)
    IV = models.ForeignKey(IndustrialVisit, on_delete=models.CASCADE, blank=False)
    date = models.DateField(default=date.today)


class Group(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False)
    IVRequest = models.ForeignKey(IVRequest, on_delete=models.CASCADE, blank=False)


class RequestNotice(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False)
    IVRequest = models.ForeignKey(IVRequest, on_delete=models.CASCADE, blank=False)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def as_dict(self):
        message = {}
        message["label"] = "iv_request"


class DoneIV(models.Model):
    IV = models.ForeignKey(IndustrialVisit, on_delete=models.CASCADE, blank=False)
    date = models.DateField(blank=False, default=date.today)


class PrevIV(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False)
    IV = models.ForeignKey(DoneIV, on_delete=models.CASCADE, blank=False)


class UpcomingIV(models.Model):
    IVRequest = models.ForeignKey(IVRequest, on_delete=models.CASCADE, blank=False)
    dateConf = models.DateField(blank=False)
    letter = models.FileField(blank=True)
