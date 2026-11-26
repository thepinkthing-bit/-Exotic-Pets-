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
]