from django.contrib.auth.models import User
from django import forms

class UlpoadFileForm(forms.Form):
    file=forms.FileField()

    def __init__(self, *args, **kwargs):
        super(UlpoadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'accept': 'image/png, image/jpeg'})