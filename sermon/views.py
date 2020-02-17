from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView, FormView, UpdateView

from core.file_uploads import file_uploads
from users import mixins as user_mixins
from . import models
from . import forms
import os

from hitcount.views import HitCountDetailView


def sermon_list(request):
    return render(request, "sermon/sermon_list.html")


class SermonDetail(DetailView):

    """ SermonDetail Definition """

    model = models.Sermon
    count_hit = True


class SermonCreateView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.SermonForm
    template_name = "sermon/sermon_create.html"

    def form_valid(self, form):
        sermon = form.save()
        sermon.author = self.request.user
        sermon.save()
        for i in self.request.FILES.getlist("photos"):
            upload_url = file_uploads(i, f"sermon/{sermon.pk}")
            models.Photo.objects.create(sermon=sermon, files=upload_url)
        messages.success(self.request, "Sermon created")
        return redirect(reverse("sermon:detail", kwargs={"pk": sermon.pk}))


class SermonEditView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Sermon
    form_class = forms.SermonForm
    template_name = "sermon/sermon_update.html"

    def form_valid(self, form):
        sermon = form.save()
        sermon.author = self.request.user
        sermon.save()
        for i in self.request.FILES.getlist("photos"):
            upload_url = file_uploads(i, f"sermon/{sermon.pk}")
            models.Photo.objects.create(sermon=sermon, files=upload_url)
        messages.success(self.request, "Sermon created")
        return redirect(reverse("sermon:detail", kwargs={"pk": sermon.pk}))

    def get_object(self, queryset=None):
        sermon = super().get_object(queryset=queryset)
        if sermon.author.pk != self.request.user.pk:
            raise Http404()
        return sermon


@login_required
def delete_photo(request, sermon_pk, photo_pk):
    user = request.user
    try:
        sermon = models.Sermon.objects.get(pk=sermon_pk)
        if sermon.author.pk != user.pk:
            data = {"message": "Cant delete that photo"}
        else:
            photo = models.Photo.objects.get(pk=photo_pk)
            filepath = settings.MEDIA_ROOT + f"{photo.files}".replace(
                "/media", ""
            ).replace("/", "\\")
            os.remove(filepath)
            photo.delete()
            data = {"message": "Photo deleted"}
        return JsonResponse(data)
    except models.Sermon.DoesNotExist:
        return redirect(reverse("core:index"))
