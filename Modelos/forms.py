from django import forms
from .models import *

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = '__all__'