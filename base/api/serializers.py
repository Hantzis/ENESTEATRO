from rest_framework import serializers
from .. models import *



class RegistroSerializer(serializers.ModelSerializer):
    #id = serializers.HyperlinkedRelatedField(read_only=True, view_name='registro-detail')
    archivo = serializers.HyperlinkedRelatedField(queryset=Archivo.objects.get(pk=pk), view_name='archivo-detail')
    fondo = serializers.StringRelatedField(read_only=True)
    lugar = serializers.StringRelatedField(read_only=True)
    usuario = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Registro
        fields = '__all__'



class ArchivoSerializer(serializers.HyperlinkedModelSerializer):
    registros = RegistroSerializer(many=True, read_only=True)
    class Meta:
        model = Archivo
        fields = '__all__'

class ArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archivo
        fields = '__all__'

class FondoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fondo
        fields = '__all__'

class LugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lugar
        fields = '__all__'

class RamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ramo
        fields = '__all__'

class FechaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fecha
        fields = '__all__'

