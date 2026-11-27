from django.conf import settings
from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Post(models.Model):
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        null=True,
        blank=True,
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    nome_cientifico = models.CharField(max_length=120, blank=True)
    imagem_capa = models.ImageField(upload_to="posts/capas/", blank=True, null=True)
    imagem_detalhe = models.ImageField(upload_to="posts/detalhes/", blank=True, null=True)
    resumo = models.TextField(max_length=300)
    conteudo = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    publicado = models.BooleanField(default=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return self.titulo


class ImagemPost(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="imagens",
    )
    imagem = models.ImageField(upload_to="posts/galeria/")
    legenda = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.legenda or f"Imagem de {self.post.titulo}"