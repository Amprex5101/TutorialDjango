from django.contrib import admin

from .models import Choice, Question, Usuario


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


class UsuarioAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["Nombre"]}),
        (None, {"fields": ["Email"], "classes": ["collapse"]}),
        (None, {"fields": ["Contrasena"], "classes": ["collapse"]}),
    ]
    search_fields = ["Nombre"]

    list_filter = ["Email"]
    search_fields = ["Nombre"]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Usuario, UsuarioAdmin)