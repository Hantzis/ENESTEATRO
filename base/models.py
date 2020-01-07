from django.contrib.gis.db import models
from django.contrib.auth.models import User
from taggit.models import TaggedItemBase, Tag as TaggitTag
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


# Create your models here.

class Archivo(models.Model):
    archivo_nombre = models.CharField(max_lenght=255, unique=True)

    def __str__(self):
        return self.archivo_nombre


class Fondo(models.Model):
    fondo_nombre = models.CharField(max_lenght=255, unique=True)

    def __str__(self):
        return self.fondo_nombre


class Lugar(models.Model):
    lugar_nombre = models.CharField(max_lenght=255, unique=True)
    lugar_geom = models.PointField()

    def __str__(self):
        return self.lugar_nombre

class Ramo(models.Model):
    ramo_nombre = models.CharField(max_lenght=255, unique=True)

    def __str__(self):
        return self.ramo_nombre

class Fecha(models.Model):
    fecha = models.DateField()

    def __str__(self):
        return self.fecha.year

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('Registro', related_name='registro_etiquetas')

class Registro(models.Model):
    archivo = models.ForeignKey(Archivo)
    fondo = models.ForeignKey(Fondo)
    libro = models.PositiveIntegerField(blank=True, null=True)
    foja = models.CharField(max_lenght=255, blank=True, null=True)
    caja = models.CharField(max_lenght=255, blank=True, null=True)
    expediente = models.CharField(max_lenght=255, blank=True, null=True)
    fechas = models.ManyToManyField(Fecha, blank=True, null=True)
    lugar = models.ForeignKey(Lugar)
    ramos = models.ManyToManyField(Ramo, null=True, blank=True)
    encabezados = models.TextField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    transcripcion = models.TextField(blank=True, null=True)
    etiquetas = ClusterTaggableManager(through='RegistroEtiqueta', blank=True)
    usuario = models.ForeignKey(User)
    fecha_registro = models.DateField(auto_now_add=True)