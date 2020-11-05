from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("view/<int:pid>", views.view, name="view"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("comment/<int:pid>", views.comment, name="comment"),
    path("addwatchlist/<int:pid>", views.addwatchlist, name="addwatchlist"),
    path("deletewatchlist/<int:pid>", views.deletewatchlist, name="deletewatchlist"),
    path("close/<int:pid>", views.close, name="close"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.get_category, name="category")

]
