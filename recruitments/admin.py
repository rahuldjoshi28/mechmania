from django.contrib import admin
from .models import recruitment, recruitmentRequest, ConfirmedRecruitment

admin.site.register(recruitment)
admin.site.register(recruitmentRequest)
admin.site.register(ConfirmedRecruitment)