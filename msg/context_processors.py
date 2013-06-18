'''
Created on 21.05.2011

@author: stefan
'''
from models import Message
def msg_stats(request):
    if (request.user.is_anonymous()):
        msg_new = 0
        msg_all = 0
    else:
        msg_new = Message.objects.filter(readed=False,reciver=request.user).count()
        msg_all = Message.objects.filter(reciver=request.user).count()
    return {'msg_new':msg_new,'msg_all':msg_all}