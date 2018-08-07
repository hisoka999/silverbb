'''
Created on 26.04.2012

@author: stefan
'''
from msg.models import Message
from django.forms import ModelForm

class MessageForm(ModelForm):
    
    class Meta:
        model = Message
        exclude ={'sender','readed','time'}