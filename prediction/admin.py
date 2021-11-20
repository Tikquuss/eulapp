from django.contrib import admin
from .models import Schedule, Team, Meeting

admin.site.register(Team)
admin.site.register(Schedule)
admin.site.register(Meeting)