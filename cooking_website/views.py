from django.views.generic import (
    TemplateView,
    CreateView,
    DetailView,
    UpdateView,
    ListView,
)
from django.contrib.auth.views import LoginView, LogoutView


class IndexView(TemplateView):
    pass


class SignUpView(CreateView):
    pass


class LoginView(LoginView):
    pass


class LogoutView(LogoutView):
    pass


class SearchView(TemplateView):
    pass


class RecipeView(DetailView):
    pass


class RecipeCreateView(CreateView):
    pass


class RecipeUpdateView(UpdateView):
    pass


class UserRecipeView(DetailView):
    pass


class UserFollowingView(ListView):
    pass


class UserFollowerView(ListView):
    pass


class UserUpdateView(UpdateView):
    pass


class NotificationView(ListView):
    pass
