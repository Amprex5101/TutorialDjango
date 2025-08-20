from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User

class Question(models.Model):
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
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
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


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # Campos adicionales que quieras agregar al usuario
    
    def __str__(self):
        return self.usuario.username
