
from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("allposts", views.allposts, name="allposts"),
    path("profile/<int:userid>", views.profile, name="profile"),
    path("follow/<int:userid>", views.follow, name="follow"),
    path("following", views.following, name="following"),

    # API Routes
    path("posts/<int:post_id>", views.edit, name="edit"),
    path("like/<int:post_id>", views.like, name="like")



]
