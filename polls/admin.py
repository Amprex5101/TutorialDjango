from django.contrib import admin
from threading import local
from django.utils.deprecation import MiddlewareMixin

from .models import Choice, Question, Vote, Modificaciones


#Sirve para mostrar las opciones de respuesta en línea dentro de la pregunta, inicia con 3 campos de llenado, de elección, se puede agregar más o eliminar.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

"""Este es el acceso Admin para manejar las preguntas y respuestas de la encuesta, permitiendo crear, editar y eliminar preguntas y opciones de respuesta.
así como también gestionar los votos y almacenar las modificaciones, creaciones de los usuarios, cuando se elimine una pregunta se eliminaran las modificaciones,
esto aun no se como arreglarlo, es una manera facil de estar controlando las actualizaciones.
"""
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date", "end_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "end_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    
    def save_model(self, request, obj, form, change):
        """Captura el usuario actual cuando se guarda un modelo desde el admin"""
        # Utiliza request.user para obtener el usuario actual
        from .Modificaciones import registrar_creacion, registrar_actualizacion

        # Guardar el modelo primero
        super().save_model(request, obj, form, change)
        
        # Registrar la acción después de guardar
        if not change:  # Es una creación
            registrar_creacion(obj, request.user)
        else:  # Es una actualización
            registrar_actualizacion(obj, request.user)
    
    def delete_model(self, request, obj):
        """Captura el usuario actual cuando se elimina un modelo desde el admin
            El problema al eliminar una pregunta es que también se eliminan las modificaciones asociadas, aun no se como resolverlo.
        """
        from .Modificaciones import registrar_eliminacion
        
        # Registrar la eliminación antes de eliminar el objeto
        registrar_eliminacion(obj, request.user)

        # Eliminar el modelo después, el problema con esto es que la modificación asociada elimina también, por lo que queda incompleta esta parte.
        super().delete_model(request, obj)
    
    def delete_queryset(self, request, queryset):
        """Maneja la eliminación de multiples preguntas, es lo mismo que la eliminación de una sola pregunta pero con multiples, y sigue habiendo el mismo problema de
        la relación, de que al momento de eliminar el modelo se eliminan las modificaciones asociadas a esa pregunta"""
        from .Modificaciones import registrar_eliminacion
        
        # Registrar cada eliminación
        for obj in queryset:
            registrar_eliminacion(obj, request.user)
            
        # Eliminar los objetos después
        super().delete_queryset(request, queryset)

class VoteAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'pregunta', 'opcion', 'fecha_voto']
    list_filter = ['fecha_voto', 'pregunta']
    search_fields = ['usuario__username', 'pregunta__question_text']
    date_hierarchy = 'fecha_voto'

class ModificacionesAdmin(admin.ModelAdmin):
    list_display = ['pregunta', 'usuario', 'tipo', 'fecha_modificacion']
    list_filter = ['tipo', 'fecha_modificacion', 'usuario']
    search_fields = ['pregunta__question_text', 'usuario__username']
    readonly_fields = ['pregunta', 'usuario', 'tipo', 'fecha_modificacion']
    date_hierarchy = 'fecha_modificacion'
    
    def has_add_permission(self, request):
        """Desactiva la posibilidad de agregar manualmente modificaciones"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Desactiva la posibilidad de modificar registros de modificación"""
        return False
    # def has_delete_permission(self, request, obj=None):
    #     """Desactiva la posibilidad de eliminar registros de modificación"""
    #     return False


admin.site.register(Vote, VoteAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Modificaciones, ModificacionesAdmin)
