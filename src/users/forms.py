from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from chat.models import UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password1',
            'password2'
        ]
    
class UserProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'languageKey', 
        ]

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username', 
            'email'
        ]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'languageKey', 
        ]
