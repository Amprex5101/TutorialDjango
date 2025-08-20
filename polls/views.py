from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils import timezone
from django.views import generic
from django.db.models import F, Sum
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Choice, Question, PerfilUsuario, Vote
from random import randrange
from .forms import UsuarioRegistroForm, UsuarioLoginForm
from django.db import IntegrityError
import datetime
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            question = self.object
            try:
                voto = Vote.objects.get(usuario=self.request.user, pregunta=question)
                context['ya_voto'] = True
                context['opcion_seleccionada'] = voto.opcion  # La opción que seleccionó
                context['fecha_voto'] = voto.fecha_voto  # Cuándo votó
            except Vote.DoesNotExist:
                context['ya_voto'] = False
                context['opcion_seleccionada'] = None
        else:
            # Si el usuario no está autenticado
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
        """Return the questions that are older than a week."""
        una_semana_atras = timezone.now() - datetime.timedelta(days=7)
        return Question.objects.filter(pub_date__lt=una_semana_atras).order_by("-pub_date")


def vote(request, question_id):
    # Verificar si el usuario está autenticado
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para votar.")
        return redirect('polls:login')
        
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
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
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
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