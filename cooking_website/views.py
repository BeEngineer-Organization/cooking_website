from django.views.generic import (
    TemplateView,
    CreateView,
    DetailView,
    UpdateView,
    ListView,
)
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import CustomUser, Recipe, Notification
from .forms import LoginForm, CustomUserForm, RecipeForm


class IndexView(TemplateView):
    template_name = "cooking_website/index.html"


class MyLoginView(LoginView):
    template_name = "cooking_website/login.html"
    form_class = LoginForm


class MyLogoutView(LoginRequiredMixin, LogoutView):
    pass


class SignUpView(CreateView):
    template_name = "cooking_website/sign_up.html"
    model = CustomUser
    form_class = CustomUserForm
    success_url = reverse_lazy("cooking_website:search")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


class SearchView(LoginRequiredMixin, TemplateView):
    template_name = "cooking_website/search.html"


class RecipeView(LoginRequiredMixin, DetailView):
    template_name = "cooking_website/recipe.html"
    model = Recipe


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "cooking_website/recipe_update.html"
    model = Recipe
    form_class = RecipeForm


class RecipeCreateView(LoginRequiredMixin, CreateView):
    template_name = "cooking_website/recipe_create.html"
    model = Recipe
    form_class = RecipeForm


class UserView(LoginRequiredMixin, DetailView):
    template_name = "cooking_website/user.html"
    model = CustomUser


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "cooking_website/user_update.html"
    model = CustomUser
    form_class = CustomUserForm


class UserFollowingView(LoginRequiredMixin, DetailView):
    template_name = "cooking_website/user_following.html"
    model = CustomUser


class UserFollowerView(LoginRequiredMixin, DetailView):
    template_name = "cooking_website/user_follower.html"
    model = CustomUser


class NotificationView(LoginRequiredMixin, ListView):
    template_name = "cooking_website/notification.html"
    model = Notification
