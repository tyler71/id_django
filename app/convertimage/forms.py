from django import forms
from .models import ConversionType

class NewImageForm(forms.Form):
    # type   = forms.ModelChoiceField(queryset=ConversionType.objects.all())
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
