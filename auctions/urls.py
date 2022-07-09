from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user_listing/<str:user>", views.user_listing, name="user_listing"),
    path("create_listing", views.create_newAuctionListing, name="create_listing"),

]
