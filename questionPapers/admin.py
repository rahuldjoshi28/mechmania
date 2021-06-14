from django.contrib import admin
from .models import Papers,PapersSearchFields
from .models import College
from .models import Subject

admin.site.register(College)
admin.site.register(Subject)
admin.site.register(Papers,PapersSearchFields)