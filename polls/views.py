from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import generic
from django.db.models import F, Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Choice, Question
from django.http import JsonResponse
from random import randrange


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

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
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


