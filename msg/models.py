from django.db import models
from django.contrib.auth.models import User
from backend.models import get_clean_text

class Message(models.Model):
    title   = models.CharField(max_length=200)
    text    = models.TextField()
    time    = models.DateTimeField(auto_now=True)
    sender  = models.ForeignKey(User,related_name='sender')
    reciver = models.ForeignKey(User,related_name='reciver')
    readed  = models.BooleanField(default=False)
    bbcode  = models.BooleanField(default=True)
    smiles  = models.BooleanField(default=True)
    
    
    def get_clean_msg(self):
        return get_clean_text(self.text)