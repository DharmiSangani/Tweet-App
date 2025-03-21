from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Tweetform(forms.ModelForm):
    class Meta:
        model=Tweet
        fields=['text', 'photo']

class UserRegistrationFrom(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=('username', 'email', 'password1', 'password2', )

class SerchForm(forms.Form):
    query=forms.CharField(label="Search", max_length=100)
