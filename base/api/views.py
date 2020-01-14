from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.generics import get_object_or_404
from . serializers import *
from django.contrib.auth.models import User

# Create your views here.

class APIRootView(generics.GenericAPIView):

    def get(self, request):
        data = {
            'archivos-lista': reverse('archivos-list')
        }
        return Response(data)




class ArchivoList(ListCreateAPIView):
    queryset = Archivo.objects.all()
    serializer_class = ArchivoSerializer


class ArchivoDetail(RetrieveUpdateDestroyAPIView):
    queryset = Archivo.objects.all()
    serializer_class = ArchivoSerializer


class FondoList(ListCreateAPIView):
    queryset = Fondo.objects.all()
    serializer_class = FondoSerializer


class FondoDetail(RetrieveUpdateDestroyAPIView):
    queryset = Fondo.objects.all()
    serializer_class = FondoSerializer


class LugarList(ListCreateAPIView):
    queryset = Lugar.objects.all()
    serializer_class = LugarSerializer


class LugarDetail(RetrieveUpdateDestroyAPIView):
    queryset = Lugar.objects.all()
    serializer_class = LugarSerializer


class RamoList(ListCreateAPIView):
    queryset = Ramo.objects.all()
    serializer_class = RamoSerializer


class RamoDetail(RetrieveUpdateDestroyAPIView):
    queryset = Ramo.objects.all()
    serializer_class = RamoSerializer


class FechaList(ListCreateAPIView):
    queryset = Fecha.objects.all()
    serializer_class = FechaSerializer


class FechaDetail(RetrieveUpdateDestroyAPIView):
    queryset = Fecha.objects.all()
    serializer_class = FechaSerializer



class RegistroList(ListCreateAPIView):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer


class RegistroDetail(RetrieveUpdateDestroyAPIView):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer
    


"""
class RegistroCreate(CreateAPIView):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer

    def perform_create(self, serializer):
        archivo_pk = self.kwargs.get('archivo_pk')
        fondo_pk = self.kwargs.get('fondo_pk')
        lugar_pk = self.kwargs.get('lugar_pk')
        usuario_pk = self.kwargs.get('usuario_pk')
        archivo = get_object_or_404(Archivo, pk=archivo_pk)
        fondo = get_object_or_404(Fondo, pk=fondo_pk)
        lugar = get_object_or_404(Lugar, pk=lugar_pk)
        usuario = get_object_or_404(Archivo, pk=usuario_pk)
        serializer.save(archivo=archivo, fondo=fondo, lugar=lugar, usuario=usuario)


class RegistroDetail(RetrieveUpdateDestroyAPIView):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer
"""

