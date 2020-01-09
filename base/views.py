from django.shortcuts import render
from . serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

# Create your views here.

class APIRootView(generics.GenericAPIView):

    def get(self, request):
        data = {
            'archivos-lista': reverse('archivos-list')
        }
        return Response(data)

class ArchivoList(generics.ListCreateAPIView):
    queryset = Archivo.objects.all()
    serializer_class = ArchivoSerializer


class ArchivoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Archivo.objects.all()
    serializer_class = ArchivoSerializer


class FondoList(generics.ListCreateAPIView):
    queryset = Fondo.objects.all()
    serializer_class = FondoSerializer


class FondoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fondo.objects.all()
    serializer_class = FondoSerializer


class LugarList(generics.ListCreateAPIView):
    queryset = Lugar.objects.all()
    serializer_class = LugarSerializer


class LugarDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lugar.objects.all()
    serializer_class = LugarSerializer


class RamoList(generics.ListCreateAPIView):
    queryset = Ramo.objects.all()
    serializer_class = RamoSerializer


class RamoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ramo.objects.all()
    serializer_class = RamoSerializer


class FechaList(generics.ListCreateAPIView):
    queryset = Fecha.objects.all()
    serializer_class = FechaSerializer


class FechaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fecha.objects.all()
    serializer_class = FechaSerializer


class RegistroList(generics.ListCreateAPIView):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer


class RegistroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer
