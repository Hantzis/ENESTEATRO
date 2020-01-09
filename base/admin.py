from django.contrib import admin
from . models import *
from django.contrib.gis.admin import OSMGeoAdmin

# Register your models here.
admin.site.register(Archivo)
admin.site.register(Fondo)
admin.site.register(Lugar, OSMGeoAdmin)
admin.site.register(Ramo)
admin.site.register(Fecha)
admin.site.register(Registro)
