from django.contrib import admin

from .models import CustomUser, Connection, Recipe

admin.site.register(CustomUser)
admin.site.register(Connection)
admin.site.register(Recipe)
