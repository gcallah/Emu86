from django.contrib import admin

# Register your models here.
from .models import AdminEmail, Site

admin.site.register(AdminEmail)
admin.site.register(Site)
