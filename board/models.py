from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from core import models as core_models

from ckeditor.fields import RichTextField
from hitcount.models import HitCountMixin


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    files = models.ImageField(upload_to="board")
    board = models.ForeignKey("Board", related_name="photos", on_delete=models.CASCADE)


class Board(core_models.TimeStampedModel, HitCountMixin):

    """ Board Model Definition """

    title = models.CharField(max_length=140)
    content = RichTextField()
    author = models.ForeignKey(
        User, related_name="board_author", on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse("board:detail", kwargs={"pk": self.pk})

    def get_photos(self):
        photos = self.photos.all()
        return photos

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.files
        except:
            return None
