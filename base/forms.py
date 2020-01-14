from django.forms import ModelForm 
from base.models import *

class RegistroForm(ModelForm):
    class Meta:
        model = Registro
        fields = '__all__'
