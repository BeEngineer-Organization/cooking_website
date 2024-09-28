from django.contrib import admin

from .models import CustomUser, Connection

admin.site.register(CustomUser)
admin.site.register(Connection)
