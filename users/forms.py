from django import forms
from .models import *
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('first_name','last_name','username','password','email')


class UserProfileInfoForm(forms.ModelForm):

    class Meta():
        model = UserProfile
        fields = ('club', 'role')

class RequestInfoForm(forms.ModelForm):
    # club = forms.CharField()
    class Meta():
        model = Request
        fields = '__all__'

class ItemInfoForm(forms.ModelForm):
    # club = forms.CharField()
    class Meta():
        model = Item
        fields = '__all__'

class ClubInfoForm(forms.ModelForm):
    # club = forms.CharField()
    class Meta():
        model = Club
        fields = '__all__'
