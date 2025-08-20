from django.contrib import admin

from .models import Choice, Question, PerfilUsuario, Vote


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date", "end_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "end_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ["usuario", "get_email"]
    search_fields = ["usuario__username", "usuario__email"]

    def get_email(self, obj):
        return obj.usuario.email

    get_email.short_description = "Email"

class VoteAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'pregunta', 'opcion', 'fecha_voto']
    list_filter = ['fecha_voto', 'pregunta']
    search_fields = ['usuario__username', 'pregunta__question_text']
    date_hierarchy = 'fecha_voto'


admin.site.register(Vote, VoteAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)