from .models import Message
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
class MessageForm(forms.ModelForm):

        img=forms.FileField(required=False)
        class Meta:
            model=Message
            fields=['title','content','img','type']

class UserForm(UserCreationForm):
    password2=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model=User
        fields=['username','email','password','password2']