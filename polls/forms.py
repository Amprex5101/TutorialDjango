from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UsuarioRegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        # Personalizar o eliminar los textos de ayuda
        help_texts = {
            'username': '',  # Eliminar el mensaje de ayuda completamente
            'email': 'Introduce un email válido',  # Personalizar el mensaje
            'password1': '',  # Eliminar mensaje de requisitos de contraseña
            'password2': '',  # Eliminar mensaje de confirmación
        }
        # También puedes personalizar las etiquetas
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Otra forma de eliminar los textos de ayuda es sobreescribiéndolos en el constructor
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        
        # También puedes personalizar los errores
        self.fields['username'].error_messages = {'required': 'Por favor introduce un nombre de usuario'}
        self.fields['email'].error_messages = {'required': 'Por favor introduce un email válido'}
        
        # Personalizar atributos de los campos, como clases CSS
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UsuarioLoginForm(AuthenticationForm):
    username = forms.CharField(label="Nombre de usuario o Email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")