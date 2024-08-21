from django import forms
from psmapp.models import Document, Subject, SubjectSuggestion
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['subject', 'file']

class SubjectSuggestionForm(forms.ModelForm):
    class Meta:
        model = SubjectSuggestion
        fields = ['suggested_subject']
    

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)
