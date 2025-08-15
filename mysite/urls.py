from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls
from polls import views

urlpatterns = [
    path('', views.index, name='index'),
    path('polls/', include("polls.urls")),
    path('admin/', admin.site.urls),
] + debug_toolbar_urls()