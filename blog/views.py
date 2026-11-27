from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ImagemPostFormSet, PostForm
from .models import Categoria, Post
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def index(request, slug=None):
    categorias = Categoria.objects.all()
    posts = Post.objects.filter(publicado=True).select_related("categoria")
    categoria_ativa = None
    query = request.GET.get("q", "").strip()

    if slug:
        categoria_ativa = get_object_or_404(Categoria, slug=slug)
        posts = posts.filter(categoria=categoria_ativa)

    if query:
        posts = posts.filter(
            Q(titulo__icontains=query)
            | Q(nome_cientifico__icontains=query)
            | Q(resumo__icontains=query)
        )

    contexto = {
        "posts": posts,
        "categorias": categorias,
        "categoria_ativa": categoria_ativa,
        "query": query,
    }
    return render(request, "index.html", contexto)


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related("categoria"),
        slug=slug,
        publicado=True,
    )
    return render(request, "post_detail.html", {"post": post})

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        formset = ImagemPostFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            post = form.save()
            formset.instance = post
            formset.save()
            if post.publicado:
                return redirect("blog:post_detail", slug=post.slug)
            return redirect("blog:index")
    else:
        form = PostForm()
        formset = ImagemPostFormSet()

    return render(
        request,
        "post_form.html",
        {"form": form, "formset": formset, "modo_edicao": False},
    )

@login_required
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        formset = ImagemPostFormSet(request.POST, request.FILES, instance=post)
        if form.is_valid() and formset.is_valid():
            post_atualizado = form.save()
            formset.save()
            if post_atualizado.publicado:
                return redirect("blog:post_detail", slug=post_atualizado.slug)
            return redirect("blog:index")
    else:
        form = PostForm(instance=post)
        formset = ImagemPostFormSet(instance=post)

    return render(
        request,
        "post_form.html",
        {"form": form, "formset": formset, "post": post, "modo_edicao": True},
    )

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        post.delete()
        return redirect("blog:index")

    return render(request, "post_confirm_delete.html", {"post": post})

def post_list(request, slug=None):
    categorias = Categoria.objects.all()
    posts = Post.objects.filter(publicado=True).select_related("categoria")
    categoria_ativa = None
    query = request.GET.get("q", "").strip()

    if slug:
        categoria_ativa = get_object_or_404(Categoria, slug=slug)
        posts = posts.filter(categoria=categoria_ativa)

    if query:
        posts = posts.filter(
            Q(titulo__icontains=query)
            | Q(nome_cientifico__icontains=query)
            | Q(resumo__icontains=query)
        )

    contexto = {
        "posts": posts,
        "categorias": categorias,
        "categoria_ativa": categoria_ativa,
        "query": query,
    }
    return render(request, "post_list.html", contexto)

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("blog:index")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})