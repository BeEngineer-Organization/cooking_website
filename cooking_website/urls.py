from django.urls import path

from . import views

app_name = "cooking_website"

urlpatterns = [
    path("", views.index, name="index"),
]
