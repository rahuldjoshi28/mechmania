from django.contrib import admin
from .models import Project,ProjectGroup,ProjectNotice,ProjectRequest,AcceptedGroup

# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectGroup)
admin.site.register(ProjectNotice)
admin.site.register(ProjectRequest)
admin.site.register(AcceptedGroup)