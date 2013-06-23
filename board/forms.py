'''
Created on 31.12.2011

@author: stefan
'''
from models import Thread,Post
from django.forms import ModelForm,Form
from django.forms.fields import ChoiceField
class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        exclude = ('author','posts','moved_from','board','closed','guest','views')

class PostThreadForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('name','user','thread','time_edited','guest_name')


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('user','thread','time_edited','guest_name')

class PostGuestForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('user','thread','time_edited')

class ThreadModForm(Form):
    CHOICES = (('C','close'),('M','move'),('d','delete') )
    options = ChoiceField(choices=CHOICES)

class MoveThreadForm(ModelForm):
    class Meta:
        model = Thread
        exclude = ('author','posts','moved_from','closed','name',)  