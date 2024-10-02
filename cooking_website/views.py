from django.views.generic import (
    TemplateView,
    CreateView,
    DetailView,
    UpdateView,
    ListView,
)
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import CustomUser, Recipe, Notification
from .forms import LoginForm, CustomUserForm, RecipeForm


class IndexView(TemplateView):
    template_name = "index.html"


class MyLoginView(LoginView):
    template_name = "login.html"
    form_class = LoginForm


class MyLogoutView(LoginRequiredMixin, LogoutView):
    pass


class SignUpView(CreateView):
    template_name = "sign_up.html"
    model = CustomUser
    form_class = CustomUserForm


class SearchView(LoginRequiredMixin, TemplateView):
    template_name = "search.html"


class RecipeView(LoginRequiredMixin, DetailView):
    template_name = "recipe.html"
    model = Recipe


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "recipe_update.html"
    model = Recipe
    form_class = RecipeForm


class RecipeCreateView(LoginRequiredMixin, CreateView):
    template_name = "recipe_create.html"
    model = Recipe
    form_class = RecipeForm


class UserView(LoginRequiredMixin, DetailView):
    template_name = "user.html"
    model = CustomUser


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "user_update.html"
    model = CustomUser
    form_class = CustomUserForm


class UserFollowingView(LoginRequiredMixin, DetailView):
    template_name = "user_following.html"
    model = CustomUser


class UserFollowerView(LoginRequiredMixin, DetailView):
    template_name = "user_follower.html"
    model = CustomUser


class NotificationView(LoginRequiredMixin, ListView):
    template_name = "notification.html"
    model = Notification
