from django import forms

class LoginForm(forms.Form):
    type     = forms.CharField(initial="login", widget=forms.HiddenInput)
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(forms.Form):
    type     = forms.CharField(initial="signup", widget=forms.HiddenInput)
    username = forms.CharField()
    email    = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)