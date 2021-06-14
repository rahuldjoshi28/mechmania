from django.db import models
from django.utils import timezone
from Accounts.models import Profile

class Notice(models.Model):
    user = models.ForeignKey(Profile, on_delete = models.CASCADE)
    header = models.CharField(max_length = 1000)
    message = models.CharField(max_length = 5000, blank = False)
    link = models.CharField(max_length = 100, blank = True)
    is_read = models.BooleanField(default = False)
    timestamp = models.DateTimeField(default = timezone.now, db_index = True)

    def __str__(self):
        return self.user.user.username+" "+self.message #+" "+self.timestamp

    def as_dict(self):
        rval = {}
        rval["label"] = "gen_notice"
        temp = {}
        temp["header"] = self.header
        temp["message"] = self.message
        temp["pk"] = self.pk
        rval["data"] = temp
        rval["timestamp"] = self.timestamp
        return rval