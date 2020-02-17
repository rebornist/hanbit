from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from core import models as core_models

from ckeditor.fields import RichTextField
from hitcount.models import HitCountMixin


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    files = models.ImageField(upload_to="sermon")
    sermon = models.ForeignKey(
        "Sermon", related_name="photos", on_delete=models.CASCADE
    )


class Sermon(core_models.TimeStampedModel, HitCountMixin):

    """ Sermon Model Definition """

    TYPE_SERMON = "sermen"
    TYPE_CONTEMPLATION = "contemplation"
    TYPE_COLUMN = "column"

    TYPE_CHOICES = (
        (TYPE_SERMON, "설교"),
        (TYPE_CONTEMPLATION, "묵상"),
        (TYPE_COLUMN, "칼럼"),
    )

    title = models.CharField(max_length=140)
    post_type = models.CharField(choices=TYPE_CHOICES, max_length=15, blank=True)
    content = RichTextField()
    author = models.ForeignKey(
        User, related_name="Sermon_author", on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse("sermon:detail", kwargs={"pk": self.pk})

    def get_photos(self):
        photos = self.photos.all()
        return photos
