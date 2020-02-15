from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView, FormView

from users import mixins as user_mixins
from . import models
from . import forms


def sermon_list(request):
    return render(request, "sermon/sermon_list.html")


class SermonDetail(DetailView):

    """ SermonDetail Definition """

    model = models.Sermon


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    model = models.Photo
    template_name = "sermon/photo_create.html"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo uploaded")
        return redirect(reverse("sermon:photos", kwargs={"pk": pk}))


class CreateSermonView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateSermonForm
    template_name = "sermon/sermon_create.html"

    def form_valid(self, form):
        sermon = form.save()
        sermon.host = self.request.user
        sermon.save()
        form.save_m2m()
        messages.success(self.request, "Sermon created")
        return redirect(reverse("sermon:detail", kwargs={"pk": sermon.pk}))
