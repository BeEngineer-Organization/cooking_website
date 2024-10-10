from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser, Recipe


class LoginForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "input"})
        self.fields["password"].widget.attrs.update({"class": "input"})


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "input"})
        self.fields["password1"].widget.attrs.update({"class": "input"})
        self.fields["password2"].widget.attrs.update({"class": "input"})
        self.fields["profile"].widget.attrs.update({"class": "text"})

    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2", "profile", "image"]


class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "input"})
        self.fields["profile"].widget.attrs.update({"class": "text"})

    class Meta:
        model = CustomUser
        fields = ["username", "profile", "image"]


class RecipeSearchForm(forms.Form):
    keyword = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "search__item", "placeholder": "キーワードで検索"}
        ),
    )


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "image", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "input"})
        self.fields["image"].widget.attrs.update({"class": "input"})
        self.fields["description"].widget.attrs.update({"class": "text"})
