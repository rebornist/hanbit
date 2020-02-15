from django import forms

from . import models


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = (
            "caption",
            "files",
        )

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        sermon = models.Sermon.objects.get(pk=pk)
        photo.sermon = sermon
        photo.save()


class CreateSermonForm(forms.ModelForm):
    class Meta:

        model = models.Sermon

        TYPE_SERMON = "sermen"
        TYPE_CONTEMPLATION = "contemplation"
        TYPE_COLUMN = "column"

        TYPE_CHOICES = (
            (TYPE_SERMON, "설교"),
            (TYPE_CONTEMPLATION, "묵상"),
            (TYPE_COLUMN, "칼럼"),
        )

        fields = (
            "title",
            "post_type",
            "content",
        )

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "id": "title", "name": "title"}
            ),
            "post_type": forms.Select(
                attrs={"class": "form-control", "id": "post_type", "name": "post_type"},
                choices=TYPE_CHOICES,
            ),
            "content": forms.Textarea(
                attrs={
                    "rows": 15,
                    "class": "form-control",
                    "id": "content",
                    "name": "content",
                }
            ),
        }

    def save(self, *args, **kwargss):
        sermon = super().save(commit=False)
        return sermon
