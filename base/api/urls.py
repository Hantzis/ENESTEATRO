from django.urls import path
from . views import *

urlpatterns = [
    path('archivos/', ArchivoList.as_view(), name='archivo-list'),
    path('archivos/<str:pk>/', ArchivoDetail.as_view(), name='archivo-detail'),

    path('fondos/', FondoList.as_view(), name='fondo-list'),
    path('fondos/<str:pk>/', FondoDetail.as_view(), name='fondo-detail'),
    path('lugares/', LugarList.as_view(), name='lugar-list'),
    path('lugares/<str:pk>/', LugarDetail.as_view(), name='lugar-detail'),
    path('ramos/', RamoList.as_view(), name='ramo-list'),
    path('ramos/<str:pk>/', RamoDetail.as_view(), name='ramo-detail'),
    path('fechas/', FechaList.as_view(), name='fecha-list'),
    path('fechas/<str:pk>/', FechaDetail.as_view(), name='fecha-detail'),
    path('registros/', RegistroList.as_view(), name='registro-list'),
    path('registros/<str:pk>/', RegistroDetail.as_view(), name='registro-detail'),
    #path('archivos/<str:archivo_pk>/registro/', RegistroCreate.as_view(), name='archivo-registro'),
    #path('registros/<str:pk>/', ArchivoDetail.as_view(), name='registro-list'),
]
