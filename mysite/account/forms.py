from dataclasses import field
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
    
    def clean_password2(self):
        '''validates if the password and password2 are same'''
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    
class ProfileEditForm(forms.ModelForm):
    birth_date = forms.DateField(input_formats=['%Y-%m-%d'],
                                 help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    class Meta:
        model = Profile
        fields = ('birth_date', 'photo')
