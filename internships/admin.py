from django.contrib import admin
from .models import industry, internship, IndustrialVisit, InternshipRequest, ConfirmedInternships, IVRequest,DoneIV,PrevIV,Group,RequestNotice, UpcomingIV

admin.site.register(industry)
admin.site.register(internship)
admin.site.register(IndustrialVisit)
admin.site.register(InternshipRequest)
admin.site.register(ConfirmedInternships)

admin.site.register(IVRequest)
admin.site.register(DoneIV)
admin.site.register(PrevIV)
admin.site.register(Group)
admin.site.register(RequestNotice)
admin.site.register(UpcomingIV)