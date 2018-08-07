from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
    
class Topic(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.question