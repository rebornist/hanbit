from django.urls import path
from . import views

app_name = "sermon"

urlpatterns = [path("", views.sermon_list, name="sermon_list")]
