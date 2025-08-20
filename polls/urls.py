from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path('get_chart/', views.get_chart, name='get_chart'),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("register/", views.user_registration, name="user_registration"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path('', views.index, name='index'),
    path('vencidas/', views.VencidasView.as_view(), name='vencidas'),
]