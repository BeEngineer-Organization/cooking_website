from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
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

from .models import CustomUser, Recipe, Connection, Notification
from .forms import LoginForm, CustomUserForm, RecipeSearchForm, RecipeForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, pk=self.request.user.pk)
        context["user"] = user

        form = RecipeSearchForm(self.request.GET)
        if form.is_valid():
            keyword = form.cleaned_data["keyword"]
            if keyword:
                popular_recipes = (
                    Recipe.objects.filter(
                        Q(title__icontains=keyword) | Q(description__icontains=keyword)
                    )
                    .annotate(like_count=Count("like"))
                    .order_by("-like_count")
                )
                new_recipes = Recipe.objects.filter(
                    Q(title__icontains=keyword) | Q(description__icontains=keyword)
                ).order_by("-created_at")
        else:
            popular_recipes = (
                Recipe.objects.all()
                .annotate(like_count=Count("like"))
                .order_by("-like_count")
            )
            new_recipes = Recipe.objects.all().order_by("-created_at")

        context["form"] = form
        context["popular_recipes"] = popular_recipes
        context["new_recipes"] = new_recipes
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context["object"]
        context["following_count"] = object.followee.all().count()
        context["follower_count"] = object.follower.all().count()
        recipes = object.recipe.all()
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
    form_class = CustomUserForm


class UserFollowingView(LoginRequiredMixin, ListView):
    template_name = "cooking_website/user_following.html"
    model = Connection
    paginate_by = 5

    def get_queryset(self):
        user_pk = self.kwargs.get("pk")
        user = get_object_or_404(CustomUser, pk=user_pk)
        query_set = Connection.objects.filter(follower=user).all()
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_pk"] = self.kwargs.get("pk")
        return context


class UserFollowerView(LoginRequiredMixin, ListView):
    template_name = "cooking_website/user_followed.html"
    model = Connection
    paginate_by = 5

    def get_queryset(self):
        user_pk = self.kwargs.get("pk")
        user = get_object_or_404(CustomUser, pk=user_pk)
        query_set = Connection.objects.filter(followee=user).all()
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_pk"] = self.kwargs.get("pk")
        return context


class NotificationView(LoginRequiredMixin, ListView):
    template_name = "cooking_website/notification.html"
    model = Notification
    paginate_by = 10

    def get_queryset(self):
        return (
            Notification.objects.filter(recipient=self.request.user)
            .all()
            .order_by("-created_at")
            .values("content", "sender")
        )


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
