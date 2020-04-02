from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['id', 'title']

        widgets = {
            'title': forms.Textarea(attrs={'class': 'my-2', 'id': 'inp', 'cols': 60, 'rows': 25})
        }

