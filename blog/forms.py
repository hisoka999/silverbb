'''
Created on 25.03.2013

@author: stefan
'''
from models import Comment
from django.forms import ModelForm
from django import forms

class CommentForm(ModelForm):
    user_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'inputbox'}),label='username')
    user_mail = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'inputbox'}),label='email')
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['user_name','user_mail','content']    
    class Meta:
        model = Comment
        fields = ("content","user_name", "user_mail", )
