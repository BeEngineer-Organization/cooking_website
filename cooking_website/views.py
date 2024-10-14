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
from .forms import LoginForm, SignUpForm, UserUpdateForm, RecipeSearchForm, RecipeForm


class IndexView(TemplateView):
    template_name = "cooking_website/index.html"


class MyLoginView(LoginView):
    template_name = "cooking_website/login.html"
    form_class = LoginForm


class MyLogoutView(LoginRequiredMixin, LogoutView):
    pass


class SignUpView(CreateView):
    template_name = "cooking_website/signup.html"
    model = CustomUser
    form_class = SignUpForm
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
        form = RecipeSearchForm(self.request.GET)
        if form.is_valid():
            keyword = form.cleaned_data["keyword"]
            if keyword:
                popular_recipes = (
                    Recipe.objects.filter(
                        Q(title__icontains=keyword) | Q(description__icontains=keyword)
                    )
                    .annotate(like_count=Count("like"))
                    .select_related("written_by")
                    .order_by("-like_count")
                    .values(
                        "pk",
                        "title",
                        "image",
                        "description",
                        "written_by__username",
                        "written_by__image",
                    )
                )
                new_recipes = (
                    Recipe.objects.filter(
                        Q(title__icontains=keyword) | Q(description__icontains=keyword)
                    )
                    .select_related("written_by")
                    .order_by("-created_at")
                    .values(
                        "pk",
                        "title",
                        "image",
                        "description",
                        "written_by__username",
                        "written_by__image",
                    )
                )

        else:
            popular_recipes = (
                Recipe.objects.all()
                .annotate(like_count=Count("like"))
                .order_by("-like_count")
                .values(
                    "pk",
                    "title",
                    "image",
                    "description",
                    "written_by__username",
                    "written_by__image",
                )
            )
            new_recipes = (
                Recipe.objects.all()
                .select_related("written_by")
                .order_by("-created_at")
                .values(
                    "pk",
                    "title",
                    "image",
                    "description",
                    "written_by__username",
                    "written_by__image",
                )
            )

        context["form"] = form
        context["popular_recipes"] = popular_recipes
        context["new_recipes"] = new_recipes
        return context


class RecipeView(LoginRequiredMixin, DetailView):
    template_name = "cooking_website/recipe.html"
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = context["object"]
        context["is_liked"] = bool(
            Like.objects.filter(recipe=recipe, given_by=self.request.user)
        )
        context["like_count"] = recipe.like.all().count()
        return context


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "cooking_website/recipe_update.html"
    model = Recipe
    form_class = RecipeForm

    def get_success_url(self):
        return reverse_lazy(
            "cooking_website:recipe", kwargs={"pk": self.kwargs.get("pk")}
        )


class RecipeCreateView(LoginRequiredMixin, CreateView):
    template_name = "cooking_website/recipe_create.html"
    model = Recipe
    form_class = RecipeForm

    def get_success_url(self):
        return reverse_lazy("cooking_website:recipe", kwargs={"pk": self.recipe_pk})

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.written_by = self.request.user
        instance.save()
        self.recipe_pk = instance.pk
        return super().form_valid(form)


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
    template_name = "cooking_website/user_following.html"
    model = Connection
    paginate_by = 5

    def get_queryset(self):
        user_pk = self.kwargs.get("pk")
        user = get_object_or_404(CustomUser, pk=user_pk)
        query_set = (
            Connection.objects.filter(follower=user)
            .all()
            .select_related("followee")
            .values("followee__pk", "followee__image", "followee__username")
        )
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
        query_set = (
            Connection.objects.filter(followee=user)
            .all()
            .select_related("follower")
            .values("follower__pk", "follower__image", "follower__username")
        )
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


def like_post(request):
    recipe = get_object_or_404(Recipe, pk=request.POST.get("recipe_pk"))
    like = Like.objects.filter(recipe=recipe, given_by=request.user)

    if like.exists():
        like.delete()
    else:
        Like.objects.create(recipe=recipe, given_by=request.user)

    context = {
        "like_count": recipe.like.all().count(),
    }
    return JsonResponse(context)


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
