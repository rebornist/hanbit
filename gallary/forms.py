from django import forms
from ckeditor.widgets import CKEditorWidget

from . import models


class GallaryForm(forms.ModelForm):
    class Meta:

        model = models.Gallary

        fields = (
            "title",
            "content",
        )

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "id": "title", "name": "title"}
            ),
            "content": CKEditorWidget(),
        }

    def save(self, *args, **kwargss):
        gallary = super().save(commit=False)
        return gallary
