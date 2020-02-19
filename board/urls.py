from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    path("", views.BoardListView.as_view(), name="board_list"),
    path("<int:pk>/", views.BoardDetail.as_view(), name="detail"),
    path("create/", views.BoardCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.BoardEditView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.delete_post, name="delete"),
    path(
        "<int:board_pk>/<int:photo_pk>/delete/",
        views.delete_photo,
        name="photo_delete",
    ),
]
