from django import forms
from ckeditor.widgets import CKEditorWidget

from . import models


class SermonForm(forms.ModelForm):
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
            "content": CKEditorWidget(),
        }

    def save(self, *args, **kwargss):
        sermon = super().save(commit=False)
        return sermon
