'''
Created on 04.02.2012

@author: stefan
'''
from django.core.management.base import BaseCommand, CommandError
from silverbb.users.models import User
from silverbb.board.models import Thread,Board
class Command(BaseCommand):
    args =''
    help = 'updates the board stats'
   
    
    def handle(self,*args,**options):
        users = User.objects.all()
        for user in users:
            profile = user.get_profile()
            profile.posts = user.post_set.count()
            profile.threads = user.thread_set.count()
            profile.save()
        threads = Thread.objects.all()
        for thread in threads:
            thread.posts = thread.post_set.count()-1
            thread.save()
        
        boards = Board.objects.all()
        for board in boards:
            board.threads = board.thread_set.count()
            threads = board.thread_set.all()
            board.posts=0
            for thread in threads:
                board.posts = board.posts+thread.posts 
            board.save()