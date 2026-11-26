from django import forms
from django.forms import inlineformset_factory
from django.utils.text import slugify
from .models import ImagemPost, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "categoria",
            "titulo",
            "slug",
            "nome_cientifico",
            "imagem_capa",
            "imagem_detalhe",
            "resumo",
            "conteudo",
            "publicado",
        ]
        widgets = {
            "resumo": forms.Textarea(attrs={"rows": 3}),
            "conteudo": forms.Textarea(attrs={"rows": 8}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].required = False

    def clean_slug(self):
        slug = (self.cleaned_data.get("slug") or "").strip()
        titulo = (self.cleaned_data.get("titulo") or "").strip()
        base_slug = slugify(slug or titulo)

        if not base_slug:
            raise forms.ValidationError("Informe um título ou slug válido.")

        final_slug = base_slug
        contador = 2
        qs = Post.objects.all()
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        while qs.filter(slug=final_slug).exists():
            final_slug = f"{base_slug}-{contador}"
            contador += 1

        return final_slug

ImagemPostFormSet = inlineformset_factory(
    Post,
    ImagemPost,
    fields=["imagem", "legenda"],
    extra=3,
    can_delete=True,
)