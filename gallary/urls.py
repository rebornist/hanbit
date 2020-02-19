from django.urls import path
from . import views

app_name = "gallary"

urlpatterns = [
    path("", views.GallaryListView.as_view(), name="gallary_list"),
    path("<int:pk>/", views.GallaryDetail.as_view(), name="detail"),
    path("create/", views.GallaryCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.GallaryEditView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.delete_post, name="delete"),
    path(
        "<int:gallary_pk>/<int:photo_pk>/delete/",
        views.delete_photo,
        name="photo_delete",
    ),
]
