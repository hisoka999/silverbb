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
    
    def clean(self):
        cleaned_data = super(PostGuestForm, self).clean()
        guest_name = cleaned_data.get("guest_name")
        confirm_code = cleaned_data.get("confirm_code")
        print confirm_code
        print (len(guest_name))
        if (len(guest_name) == 0):
            msg = "The Name can not be empty"
            self._errors["guest_name"] = self.error_class([msg])
            del cleaned_data["guest_name"]
        return cleaned_data

class ThreadModForm(Form):
    CHOICES = (('C','close'),('M','move'),('d','delete') )
    options = ChoiceField(choices=CHOICES)

class MoveThreadForm(ModelForm):
    class Meta:
        model = Thread
        exclude = ('author','posts','moved_from','closed','name',)  