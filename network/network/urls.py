
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addPost", views.addPost, name="addPost"),
    path("profile/<int:postUserID>/", views.profile, name="profile"),
    path("follow/<int:requestUserID>/<int:postUserID>/", views.follow, name="follow"),
    path("unfollow/<int:requestUserID>/<int:postUserID>/", views.unfollow, name="unfollow"),
    path("following/<int:userID>/", views.following, name="following"),
    
    #API routes
    path("posts/<int:postID>/", views.postJSON, name="postJSON"),
]
