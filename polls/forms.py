from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'

class UsuarioLoginForm(forms.Form):
    email = forms.EmailField()
    Contrasena = forms.CharField(widget=forms.PasswordInput)