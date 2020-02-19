from django.urls import path
from . import views

app_name = "sermon"

urlpatterns = [
    path("", views.SermonListView.as_view(), name="sermon_list"),
    path("<int:pk>/", views.SermonDetail.as_view(), name="detail"),
    path("create/", views.SermonCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.SermonEditView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.delete_post, name="delete"),
    path(
        "<int:sermon_pk>/<int:photo_pk>/delete/",
        views.delete_photo,
        name="photo_delete",
    ),
]
