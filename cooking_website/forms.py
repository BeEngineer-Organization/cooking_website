from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser, Recipe


class LoginForm(AuthenticationForm):
    pass


class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2", "profile", "image"]


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "image", "description"]
