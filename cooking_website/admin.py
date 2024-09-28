from django.contrib import admin

from .models import CustomUser, Connection, Recipe, Like

admin.site.register(CustomUser)
admin.site.register(Connection)
admin.site.register(Recipe)
admin.site.register(Like)
