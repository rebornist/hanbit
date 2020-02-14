from django.urls import path
from . import views

app_name = "awake"

urlpatterns = [path("", views.awake, name="awake")]
