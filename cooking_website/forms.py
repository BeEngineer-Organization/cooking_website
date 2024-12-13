from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser, Recipe


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "profile", "image"]


class LoginForm(AuthenticationForm):
    pass


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "profile", "image"]


class RecipeSearchForm(forms.Form):
    pass


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "image", "description"]
