'''
Created on 02.01.2012

@author: stefan
'''
from models import UserProfile
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(ModelForm):
    email2 = forms.EmailField(label="EMail (again)")
    password2 = forms.CharField( widget=forms.PasswordInput, label="Password (again)" )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['username','password','password2','email','email2']    
    class Meta:
        model = User
        fields = ("username","password", "email", )

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if (password != password2):
            msg = "Both passwords must be equal."
            self._errors["password2"] = self.error_class([msg])
            del cleaned_data["password"]
            del cleaned_data["password2"]
        
        email = cleaned_data.get("email")
        email2 = cleaned_data.get("email2")
        if (email != email2):
            msg = "Both e-mail adresses must be equal."
            self._errors["email2"] = self.error_class([msg])
            del cleaned_data["email"]
            del cleaned_data["email2"]
        
        return cleaned_data
        
class UserEditForm(ModelForm):
    
    class Meta:
        model = User
        fields = ("first_name","last_name","email")


class ProfileForm(ModelForm):
    
    class Meta:
        model = UserProfile
        exclude = ('user','posts','threads','banned','activate')