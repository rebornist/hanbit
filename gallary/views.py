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
import shutil

from hitcount.views import HitCountDetailView


class GallaryListView(ListView):

    """ HomeView Definition """

    model = models.Gallary
    paginate_by = 20
    paginate_orphans = 5
    ordering = "created"


class GallaryDetail(HitCountDetailView, DetailView):

    """ GallaryDetail Definition """

    model = models.Gallary
    count_hit = True


class GallaryCreateView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.GallaryForm
    template_name = "gallary/gallary_create.html"

    def form_valid(self, form):
        gallary = form.save()
        gallary.author = self.request.user
        gallary.save()
        for i in self.request.FILES.getlist("photos"):
            upload_url = file_uploads(i, "gallary/{}".format(gallary.pk))
            models.Photo.objects.create(gallary=gallary, files=upload_url)
        return redirect(reverse("gallary:detail", kwargs={"pk": gallary.pk}))


class GallaryEditView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Gallary
    form_class = forms.GallaryForm
    template_name = "gallary/gallary_update.html"

    def form_valid(self, form):
        gallary = form.save()
        gallary.author = self.request.user
        gallary.save()
        for i in self.request.FILES.getlist("photos"):
            upload_url = file_uploads(i, "gallary/{}".format(gallary.pk))
            models.Photo.objects.create(gallary=gallary, files=upload_url)
        return redirect(reverse("gallary:detail", kwargs={"pk": gallary.pk}))

    def get_object(self, queryset=None):
        gallary = super().get_object(queryset=queryset)
        if gallary.author.pk != self.request.user.pk:
            raise Http404()
        return gallary


@login_required
def delete_post(request, pk):
    user = request.user
    gallary = models.Gallary.objects.get(pk=pk)

    if gallary.author.pk != user.pk:
        messages.error(request, "Cant delete that post")
    else:
        gallary.delete()
        media_root = os.path.join(settings.MEDIA_ROOT, "{0}/{1}".format("gallary", pk))
        shutil.rmtree(media_root)
        messages.success(request, "Successfully deleted post")
    return redirect(reverse("gallary:gallary_list"))


@login_required
def delete_photo(request, gallary_pk, photo_pk):
    user = request.user
    try:
        gallary = models.Gallary.objects.get(pk=gallary_pk)
        if gallary.author.pk != user.pk:
            data = {"message": "Cant delete that photo"}
        else:
            photo = models.Photo.objects.get(pk=photo_pk)
            filepath = settings.MEDIA_ROOT + "{}".format(photo.files).replace(
                "/media", ""
            )
            os.remove(filepath)
            photo.delete()
            data = {"message": "Successfully deleted photo"}
        return JsonResponse(data)
    except models.Gallary.DoesNotExist:
        return redirect(reverse("core:index"))
