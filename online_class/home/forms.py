from home.models import UserProfile
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your new password...', 'title':'Ensure this value has at least 8 characters'}), min_length=8, max_length=50, error_messages={'required': 'Please enter your new password.'})
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your new password again...', 'title':'Ensure this value has at least 8 characters'}), max_length=50, error_messages={'required': 'Please re-enter your new password for confirmation.'})
    class Meta:
        model=User
        fields=('username','password','confirm_password','email','first_name','last_name')
        widgets = {
            'username': forms.TextInput(attrs=({'placeholder': 'Choose a new username...'})),
            'email': forms.TextInput(attrs=({'placeholder': 'Email address...'})),
            'first_name': forms.TextInput(attrs=({'placeholder': 'First name...'})),
            'last_name': forms.TextInput(attrs=({'placeholder': 'Last name...'})),
        }
        error_messages = {
            'username': {'required': 'Please choose a username.'},
            'gender': {'required': 'Please specify your gender.'}
        }    
    
    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        if 'password' in self.cleaned_data and self.cleaned_data['password'] != confirm_password:
            raise forms.ValidationError("Your new password and confirm password didn't matched.")        
        return confirm_password
            
class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=['user']    
class EditProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=['user'] 
        fields=('birthday','address','phone','gender','user_image')

class EditUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your new password...', 'title':'Ensure this value has at least 8 characters'}), required=False, min_length=8, max_length=50, error_messages={'required': 'Please enter your new password.'})
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your new password again...', 'title':'Ensure this value has at least 8 characters'}), required=False, max_length=50, error_messages={'required': 'Please re-enter your new password for confirmation.'})
    class Meta:
        model=User
        fields=('username','password','confirm_password','email','first_name','last_name')
        widgets = {
            'username': forms.TextInput(attrs=({'placeholder': 'Choose a new username...'})),
            'email': forms.TextInput(attrs=({'placeholder': 'Email address...'})),
            'first_name': forms.TextInput(attrs=({'placeholder': 'First name...'})),
            'last_name': forms.TextInput(attrs=({'placeholder': 'Last name...'})),
        }
        error_messages = {
            'username': {'required': 'Please choose a username.'},
            'gender': {'required': 'Please specify your gender.'}
        }    
    
    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        if 'password' in self.cleaned_data and self.cleaned_data['password'] != confirm_password:
            raise forms.ValidationError("Your new password and confirm password didn't matched.")        
        return confirm_password
    class Meta:
        model=User
        fields=('email','first_name','last_name')
