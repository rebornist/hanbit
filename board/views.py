from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, reverse
from django.views.generic import DetailView, FormView, ListView, UpdateView

from core.file_uploads import file_uploads
from users import mixins as user_mixins
from . import models
from . import forms
import os

from hitcount.views import HitCountDetailView


class BoardListView(ListView):

    """ HomeView Definition """

    model = models.Board
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"


class BoardDetail(HitCountDetailView, DetailView):

    """ BoardDetail Definition """

    model = models.Board
    count_hit = True


class BoardCreateView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.BoardForm
    template_name = "board/board_create.html"

    def form_valid(self, form):
        board = form.save()
        board.author = self.request.user
        board.save()
        for i in self.request.FILES.getlist("photos"):
            upload_url = file_uploads(i, "board/{}".format(board.pk))
            models.Photo.objects.create(board=board, files=upload_url)
        return redirect(reverse("board:detail", kwargs={"pk": board.pk}))


class BoardEditView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Board
    form_class = forms.BoardForm
    template_name = "board/board_update.html"

    def form_valid(self, form):
        board = form.save()
        board.author = self.request.user
        board.save()
        for i in self.request.FILES.getlist("photos"):
            upload_url = file_uploads(i, "board/{}".format(board.pk))
            models.Photo.objects.create(board=board, files=upload_url)
        return redirect(reverse("board:detail", kwargs={"pk": board.pk}))

    def get_object(self, queryset=None):
        board = super().get_object(queryset=queryset)
        if board.author.pk != self.request.user.pk:
            raise Http404()
        return board


@login_required
def delete_post(request, pk):
    user = request.user
    board = models.Board.objects.get(pk=pk)

    if board.author.pk != user.pk:
        messages.error(request, "Cant delete that post")
    else:
        board.delete()
        messages.success(request, "Successfully deleted post")
    return redirect(reverse("board:board_list"))


@login_required
def delete_photo(request, board_pk, photo_pk):
    user = request.user
    try:
        board = models.Board.objects.get(pk=board_pk)
        if board.author.pk != user.pk:
            data = {"message": "Cant delete that photo"}
        else:
            photo = models.Photo.objects.get(pk=photo_pk)
            filepath = settings.MEDIA_ROOT + "{}".format(photo.files).replace(
                "/media", ""
            ).replace("/", "\\")
            os.remove(filepath)
            photo.delete()
            data = {"message": "Successfully deleted photo"}
        return JsonResponse(data)
    except models.Board.DoesNotExist:
        return redirect(reverse("core:index"))
