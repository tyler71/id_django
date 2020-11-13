from django import forms

class NewImageForm(forms.Form):
    conversion_choices = (
        ('Median', 'Median'),
        ('Mean',   'Mean'),
        ('Mode',   'Mode'),
    )
    type   = forms.ChoiceField(choices=conversion_choices)
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
