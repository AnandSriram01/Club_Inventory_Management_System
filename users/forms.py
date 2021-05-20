from django import forms
from .models import UserProfile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('first_name','last_name','username','password','email')


class UserProfileInfoForm(forms.ModelForm):
    # club = forms.CharField()
    class Meta():
        model = UserProfile
        fields = ('club',)
