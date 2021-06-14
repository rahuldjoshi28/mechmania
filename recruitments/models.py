from django.db import models
from internships.models import industry
from Accounts.models import Profile

class recruitment(models.Model):
    industry = models.ForeignKey(industry, on_delete = models.CASCADE, blank=False)
    type = models.CharField(max_length =1000)
    salary = models.IntegerField()
    description = models.CharField(max_length =10000)
    qualifications = models.CharField(max_length =500)
    def __str__(self):
        return self.industry.name +" "+self.type+" "+ str(self.pk)

class recruitmentRequest(models.Model):
    user = models.ForeignKey(Profile, on_delete = models.CASCADE, blank = False)
    recruitment = models.ForeignKey(recruitment, on_delete = models.CASCADE, blank = False)

class ConfirmedRecruitment(models.Model):
    user = models.ForeignKey(Profile, on_delete = models.CASCADE, blank = False)
    recruitment = models.ForeignKey(recruitment, on_delete = models.CASCADE, blank = False)
