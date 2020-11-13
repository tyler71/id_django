from django import forms

class NewImageForm(forms.Form):
    conversion_choices = (
        ('Median', 'Median'),
        ('Mean',   'Mean'),
        ('Mode',   'Mode'),
    )
    type   = forms.ChoiceField(choices=conversion_choices)
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
