from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from threading import local
import logging
from .models import Modificaciones as ModificacionesModel, Question

# Configurar logging
logger = logging.getLogger(__name__)

def registrar_creacion(pregunta, usuario):
    """Registra la creación de una nueva pregunta."""
    logger.info(f"Registrando CREACIÓN - Pregunta: {pregunta.id}, Usuario: {usuario.username}")
    ModificacionesModel.objects.create(
        pregunta=pregunta,
        usuario=usuario,
        tipo='CREAR'
    )

def registrar_actualizacion(pregunta, usuario):
    """Registra la actualización de una pregunta existente."""
    logger.info(f"Registrando ACTUALIZACIÓN - Pregunta: {pregunta.id}, Usuario: {usuario.username}")
    ModificacionesModel.objects.create(
        pregunta=pregunta,
        usuario=usuario,
        tipo='ACTUALIZAR'
    )

def registrar_eliminacion(pregunta, usuario):
    """Registra la eliminación de una pregunta."""
    logger.info(f"Registrando ELIMINACIÓN - Pregunta: {pregunta.id}, Usuario: {usuario.username}")
    ModificacionesModel.objects.create(
        pregunta=pregunta,
        usuario=usuario,
        tipo='ELIMINAR'
    )

