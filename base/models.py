from django.contrib.gis.db import models
from django.contrib.auth.models import User
from taggit.models import TaggedItemBase, Tag as TaggitTag
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from modelcluster.models import ClusterableModel
import uuid
from crum import get_current_user


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


# Create your models here.

class Archivo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    archivo_nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.archivo_nombre


class Fondo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fondo_nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.fondo_nombre


class Lugar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lugar_nombre = models.CharField(max_length=255, unique=True)
    lugar_geom = models.PointField()

    def __str__(self):
        return self.lugar_nombre

class Ramo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ramo_nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.ramo_nombre

class Fecha(models.Model):
    fecha = models.DateField()

    def __str__(self):
        return str(self.fecha.year)

class RegistroEtiqueta(TaggedItemBase):
    content_object = ParentalKey('Registro', related_name='registro_etiquetas')

class Registro(ClusterableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    archivo = models.ForeignKey(Archivo, on_delete=models.PROTECT)
    fondo = models.ForeignKey(Fondo, on_delete=models.PROTECT)
    libro = models.PositiveIntegerField(blank=True, null=True)
    foja = models.CharField(max_length=255, blank=True, null=True)
    caja = models.CharField(max_length=255, blank=True, null=True)
    expediente = models.CharField(max_length=255, blank=True, null=True)
    fechas = models.ManyToManyField(Fecha, blank=True)
    lugar = models.ForeignKey(Lugar, on_delete=models.PROTECT)
    ramos = models.ManyToManyField(Ramo, blank=True)
    encabezado = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    transcripcion = models.TextField(blank=True, null=True)
    etiquetas = ClusterTaggableManager(through='RegistroEtiqueta', blank=True)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    fecha_registro = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Registro, self).save(*args, **kwargs)
