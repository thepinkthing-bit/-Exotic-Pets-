from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("categoria/<slug:slug>/", views.index, name="categoria"),
    path("post/novo/", views.post_create, name="post_create"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("post/<slug:slug>/editar/", views.post_update, name="post_update"),
    path("post/<slug:slug>/excluir/", views.post_delete, name="post_delete"),
    path("artigos/", views.post_list, name="post_list"),
    path(
        "conta/entrar/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("conta/sair/", auth_views.LogoutView.as_view(), name="logout"),
    path("conta/registar/", views.signup, name="signup"),
]