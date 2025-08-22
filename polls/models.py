from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User


"""
Este documento sirve para crear nuestros modelos de base de datos por medio de la librería Django.
Aquí definimos las estructuras de datos que utilizaremos en nuestra aplicación.
Tambien se definen las relaciones, cuando un campo esta relacionado por una clave foránea y encima tiene 
un nombre de una clase, significa que hay relación. Las clases son los nombres de nuestras tablas, solo que 
al ser agregadas se pone todo en minusculas.
"""
class Question(models.Model):
    """Modelo que representa una pregunta en la encuesta así como tambien la fecha de publicación y finalización."""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    end_date = models.DateTimeField("end date", null=True, blank=True)  # Agregar este campo
    def __str__(self):
        return self.question_text
    
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    """Modelo que representa las opciones disponibles para una pregunta. Esta clase está relacionada con la clase Question."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    """Modelo que representa los votos hechos por los usuarios, relaciona al usuario, la pregunta y la opción votada."""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Question, on_delete=models.CASCADE)
    opcion = models.ForeignKey(Choice, on_delete=models.CASCADE)
    fecha_voto = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Asegurar que un usuario solo pueda votar una vez por pregunta
        unique_together = ('usuario', 'pregunta')
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'
    
    def __str__(self):
        return f"{self.usuario.username} votó por '{self.opcion.choice_text}' en '{self.pregunta.question_text}'"



class Modificaciones(models.Model):
    TIPO_MODIFICACION = (
        ('CREAR', 'Crear'),
        ('ACTUALIZAR', 'Actualizar'),
        ('ELIMINAR', 'Eliminar'),
    )
    pregunta = models.ForeignKey(Question, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_MODIFICACION)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Modificación'
        verbose_name_plural = 'Modificaciones'

    def __str__(self):
        return f"Modificación de {self.pregunta.question_text} por {self.usuario.username} en {self.fecha_modificacion}"