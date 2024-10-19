from django.db.models.base import Model as Model
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
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.http import JsonResponse

from .models import CustomUser, Recipe, Connection, Like, Notification
from .forms import LoginForm, SignupForm, UserUpdateForm, RecipeSearchForm, RecipeForm


class IndexView(TemplateView):
    template_name = "cooking_website/index.html"


class SignupView(CreateView):
    template_name = "cooking_website/signup.html"
    model = CustomUser
    form_class = SignupForm
    success_url = reverse_lazy("cooking_website:search")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


class MyLoginView(LoginView):
    template_name = "cooking_website/login.html"
    form_class = LoginForm


class MyLogoutView(LoginRequiredMixin, LogoutView):
    pass


class SearchView(LoginRequiredMixin, TemplateView):
    pass


class RecipeView(LoginRequiredMixin, DetailView):
    pass


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "cooking_website/recipe_update.html"
    model = Recipe
    form_class = RecipeForm

    def get_success_url(self):
        return reverse_lazy(
            "cooking_website:recipe", kwargs={"pk": self.kwargs.get("pk")}
        )


class RecipeCreateView(LoginRequiredMixin, CreateView):
    pass


class UserView(LoginRequiredMixin, DetailView):
    template_name = "cooking_website/user.html"
    model = CustomUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context["object"]
        context["following_count"] = object.followee.all().count()
        context["follower_count"] = object.follower.all().count()
        recipes = object.recipe.all().values("pk", "title", "image")
        context["recipes"] = recipes
        context["recipe_count"] = recipes.count()

        if object is not self.request.user:
            context["is_followed"] = bool(
                Connection.objects.filter(followee=object, follower=self.request.user)
            )
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "cooking_website/user_update.html"
    model = CustomUser
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse_lazy(
            "cooking_website:user", kwargs={"pk": self.kwargs.get("pk")}
        )


class UserFollowingView(LoginRequiredMixin, ListView):
    pass


class UserFollowerView(LoginRequiredMixin, ListView):
    pass


class NotificationView(LoginRequiredMixin, ListView):
    pass


def follow_post(request):
    followee = get_object_or_404(CustomUser, pk=request.POST.get("followee_pk"))
    connection = Connection.objects.filter(followee=followee, follower=request.user)

    if connection.exists():
        connection.delete()
        method = "delete"
    else:
        Connection.objects.create(followee=followee, follower=request.user)
        method = "create"

    context = {
        "follower_count": followee.follower.all().count(),
        "method": method,
    }
    return JsonResponse(context)
