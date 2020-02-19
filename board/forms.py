from django import forms
from ckeditor.widgets import CKEditorWidget

from . import models


class BoardForm(forms.ModelForm):
    class Meta:

        model = models.Board

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
        board = super().save(commit=False)
        return board
