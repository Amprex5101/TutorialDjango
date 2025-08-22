from django.apps import AppConfig


class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
    
    def ready(self):
        # Importar el módulo de señales cuando la aplicación esté lista
        import polls.Modificaciones  # Importa las señales
