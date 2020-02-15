from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from core import models as core_models


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    files = models.ImageField(upload_to="sermon_photos")
    room = models.ForeignKey("Sermon", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Sermon(core_models.TimeStampedModel):

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
    gender = models.CharField(choices=TYPE_CHOICES, max_length=15, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, related_name="Sermons", on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("sermon:detail", kwargs={"pk": self.pk})

    def photos(self):
        photos = self.photos.all()
        return photos
