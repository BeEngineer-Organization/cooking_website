from typing import Any
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser, Recipe


class LoginForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "input"})
        self.fields["password"].widget.attrs.update({"class": "input"})


class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2", "profile", "image"]


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "image", "description"]
