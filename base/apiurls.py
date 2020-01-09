from django.urls import path
from . views import *

urlpatterns = [
    path('archivos/', ArchivoList.as_view(), name='archivos-list'),
    path('archivos/<str:pk>/', ArchivoDetail.as_view(), name='archivos-detail'),
    path('fondos/', FondoList.as_view(), name='fondos-list'),
    path('fondos/<str:pk>/', FondoDetail.as_view(), name='fondos-detail'),
    path('lugares/', LugarList.as_view(), name='lugares-list'),
    path('lugares/<str:pk>/', LugarDetail.as_view(), name='lugares-detail'),
    path('ramos/', RamoList.as_view(), name='ramos-list'),
    path('ramos/<str:pk>/', RamoDetail.as_view(), name='ramos-detail'),
    path('fechas/', FechaList.as_view(), name='fechas-list'),
    path('fechas/<str:pk>/', FechaDetail.as_view(), name='fechas-detail'),
    path('registros/', RegistroList.as_view(), name='registros-list'),
    path('registros/<str:pk>/', RegistroDetail.as_view(), name='registros-detail'),
]
