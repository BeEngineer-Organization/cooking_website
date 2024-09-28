from django.urls import path

from . import views

app_name = "cooking_website"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("sign-up", views.SignUpView.as_view(), name="sign_up"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("search", views.SearchView.as_view(), name="search"),
    path("recipe", views.RecipeView.as_view(), name="recipe"),
    path("recipe/create", views.RecipeCreateView.as_view(), name="recipe_create"),
    path("recipe/update", views.RecipeUpdateView.as_view(), name="recipe_update"),
    path("user/recipe", views.UserRecipeView.as_view(), name="user_recipe"),
    path("user/following", views.UserFollowingView.as_view(), name="user_following"),
    path("user/follower", views.UserFollowerView.as_view(), name="user_follower"),
    path("user/update", views.UserUpdateView.as_view(), name="user_update"),
    path("notification", views.NotificationView.as_view(), name="notification"),
]
