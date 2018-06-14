'''
Created on 21.05.2011

@author: stefan
'''
from django.contrib.auth import forms
def user_auth(request):
    form = forms.AuthenticationForm
    
    return {'auth_form':form}