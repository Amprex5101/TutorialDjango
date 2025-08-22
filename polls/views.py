from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils import timezone
from django.views import generic
from django.db.models import F, Sum
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Choice, Question, Vote
from random import randrange
from .forms import UsuarioRegistroForm, UsuarioLoginForm
from django.db import IntegrityError
import datetime
from django.db import models 


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the active questions (published and not ended)."""
        now = timezone.now()
        return Question.objects.filter(
            models.Q(pub_date__lte=now) & 
            (models.Q(end_date__gt=now) | models.Q(end_date=None))
        ).order_by("-pub_date")[:5]
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.object
        
        # Verificar si la encuesta está activa
        now = timezone.now()
        is_active = now >= question.pub_date and (question.end_date is None or now <= question.end_date)
        context['is_active'] = is_active
        
        if self.request.user.is_authenticated:
            try:
                voto = Vote.objects.get(usuario=self.request.user, pregunta=question)
                context['ya_voto'] = True
                context['opcion_seleccionada'] = voto.opcion
                context['fecha_voto'] = voto.fecha_voto
            except Vote.DoesNotExist:
                context['ya_voto'] = False
                context['opcion_seleccionada'] = None
        else:
            context['ya_voto'] = False
            context['opcion_seleccionada'] = None
        
        return context


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


class VencidasView(generic.ListView):
    template_name = "polls/vencidas.html"
    context_object_name = "vencidas_list"

    def get_queryset(self):
        """Return questions that have ended."""
        now = timezone.now()
        return Question.objects.filter(
            models.Q(end_date__lt=now) & models.Q(pub_date__lte=now)
        ).order_by("-end_date")


def vote(request, question_id):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para votar.")
        return redirect('polls:login')
        
    question = get_object_or_404(Question, pk=question_id)
    
    # Verificar si la encuesta está activa
    # Calcula si la encuesta está activa con respecto a la fecha de publicacion y la de
    # finalización
    now = timezone.now()
    is_active = now >= question.pub_date and (question.end_date is None or now <= question.end_date)
    #Si no esta activa en la vista detail.html aparecera un mensaje de error.
    if not is_active:
        messages.error(request, "Esta encuesta ya no está disponible para votar.")
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Esta encuesta ya no está disponible para votar.",
                "is_active": False
            },
        )
    #Si esta activa muestra el formulario con las respuestas de la encuesta
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    #Si no se selecciona nada redirigue a la misma pagina mostrando un mensaje de error
    except (KeyError, Choice.DoesNotExist):
        # Mostrar de nuevo el formulario de votación
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "No seleccionaste una opción.",
            },
        )
    #Si sí se selecciono se guardara el voto del usuario en la BD
    try:
        # Intentar registrar el voto del usuario
        vote = Vote(
            usuario=request.user,
            pregunta=question,
            opcion=selected_choice
        )
        vote.save()
        
        # Incrementar el contador de votos
        selected_choice.votes += 1
        selected_choice.save()
        
        messages.success(request, "¡Tu voto ha sido registrado!")
    #Si el usuario ya voto mostrara un mensaje de error
    except IntegrityError:
        # Si el usuario ya votó en esta pregunta
        messages.error(request, "Ya has votado en esta encuesta.")
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Ya has votado en esta encuesta anteriormente.",
            },
        )
        
    # Siempre redireccionar después de un POST exitoso
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    

def index(request):
    now = timezone.now()
    # Filtrar para obtener solo encuestas activas
    active_questions = Question.objects.filter(
        models.Q(pub_date__lte=now) & 
        (models.Q(end_date__gt=now) | models.Q(end_date=None))
    ).order_by("-pub_date")[:5]
    
    context = {"latest_question_list": active_questions}
    return render(request, "polls/index.html", context)


def get_chart(request):
    questions = Question.objects.all()
    charts_data = {}
    
    for question in questions:
        choices = question.choice_set.all()
        
        # Datos para esta pregunta específica
        chart_data = {
            'question_text': question.question_text,
            'question_id': question.id,
            'categories': [],
            'values': []
        }
        
        # Obtener las opciones y los votos
        for choice in choices:
            chart_data['categories'].append(choice.choice_text)
            chart_data['values'].append(choice.votes)
        
        # Configuración del gráfico para esta pregunta
        option = {
            'title': {
                'text': question.question_text
            },
            'tooltip': {
                'trigger': 'axis',
                'formatter': '{b}: {c} votos'
            },
            'xAxis': {
                'type': 'category',
                'data': chart_data['categories']
            },
            'yAxis': {
                'type': 'value',
                'name': 'Votos'
            },
            'series': [{
                'data': chart_data['values'],
                'type': 'bar',
                'showBackground': True,
                'itemStyle': {
                    'color': '#6b48ff'
                }
            }]
        }
        
        charts_data[question.id] = option
    
    return JsonResponse(charts_data)


def user_registration(request):
    if request.method == "POST":
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro exitoso.")
            return redirect("polls:index")
        messages.error(request, "Registro fallido. Información inválida.")
    else:
        form = UsuarioRegistroForm()
    return render(request, "polls/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = UsuarioLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Has iniciado sesión como {username}.")
                return redirect("polls:index")
            else:
                messages.error(request, "Usuario o contraseña inválidos.")
        else:
            messages.error(request, "Usuario o contraseña inválidos.")
    else:
        form = UsuarioLoginForm()
    return render(request, "polls/login.html", {"form": form})



def user_logout(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect("polls:index")