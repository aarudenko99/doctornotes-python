from django import forms


class SendEmailForm(forms.Form):
    subject = forms.CharField(max_length=200, label='Reference/Note Id',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    send_from = forms.EmailField(required=False)
    send_to = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    checkboxes = forms.CharField(widget=forms.HiddenInput, required=False)
    message = forms.CharField(widget=forms.Textarea(
        attrs={
            'rows': 21,
            'cols': 100,
            'class': 'dngOutputContent',
            'id': 'dngClipBoardText',
            'readonly': 'true'
        }
    ))


class SendRecommendationForm(forms.Form):
    subject = forms.CharField(
        max_length=200,
        label='Note name',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'readonly': True})
    )
    message = forms.CharField(widget=forms.Textarea(
        attrs={
            'rows': 3,
            'class': 'form-control',
        }
    ))
    note_id = forms.IntegerField(widget=forms.HiddenInput())


class SaveDraftForm(SendEmailForm):
    send_to = forms.EmailField(
        required=False, widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
