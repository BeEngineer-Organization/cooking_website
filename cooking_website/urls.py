from django.urls import path

from . import views

app_name = "cooking_website"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("login", views.MyLoginView.as_view(), name="login"),
    path("logout", views.MyLogoutView.as_view(), name="logout"),
    path("search", views.SearchView.as_view(), name="search"),
    path("recipe/<int:pk>", views.RecipeView.as_view(), name="recipe"),
    path(
        "recipe/<int:pk>/update", views.RecipeUpdateView.as_view(), name="recipe_update"
    ),
    path("recipe/create", views.RecipeCreateView.as_view(), name="recipe_create"),
    path("user/<int:pk>", views.UserView.as_view(), name="user"),
    path("user/<int:pk>/update", views.UserUpdateView.as_view(), name="user_update"),
    path(
        "user/<int:pk>/following",
        views.UserFollowingView.as_view(),
        name="user_following",
    ),
    path(
        "user/<int:pk>/follower", views.UserFollowerView.as_view(), name="user_follower"
    ),
    path("notification", views.NotificationView.as_view(), name="notification"),
    path("like-post", views.like_post, name="like_post"),
    path("follow-post", views.follow_post, name="follow_post"),
]
