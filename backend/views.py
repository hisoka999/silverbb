# Create your views here.
from backend.functions import render_to_response
from django.template import RequestContext
from django.http.response import HttpResponse
from django.conf import settings
from users.models import UserSession

def show_css(request,css_file1):
    #print 'css/'+css_file+'.css'
    print(request.user)
    return render_to_response('css/'+css_file1+'.css',{},context_instance=RequestContext(request),mimetype="text/css")


def show404(request):
    """
    404 error handler.

    Templates: `404.html`
    Context: None
    """
    return render_to_response('404.html',
        context_instance = RequestContext(request)
    )
    
    
def captcha(request):
    ''' A View that Returns a PNG Image generated using PIL'''
    #import PIL
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    import random
    random.seed()
    size = (200,70)             # size of the image to create
    im = Image.new('RGB', size) # create the image
    draw = ImageDraw.Draw(im)   # create a drawing object that is
                                # used to draw on the new image
    FONTS = ["ArchitectsDaughter","arial","minya"]
    CHARACTERS = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
                  ,'a','b','c','d','e','f','g','h','i','j','k','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    
    #draw.setFont(font)
    white = (random.randint(200,255),random.randint(200,255),random.randint(200,255)) # color of the background
    text_pos = (10,20) # top-left position of our text
    text = "" # text to draw
    # Now, we'll do the drawing:
    draw.rectangle([(0,0),size],fill=white)
    for i in range(0,10,1):
        font = ImageFont.truetype(settings.PROJECT_ROOT+"/fonts/"+FONTS[random.randrange(len(FONTS))]+".ttf", random.randint(20,25))
        char = CHARACTERS[random.randrange(len(CHARACTERS))]
        text=text+char
        font_size = font.getsize(char)[0]
        if font_size < 15:
            font_size = 15
        text_color = (random.randint(0,155),random.randint(0,155),random.randint(0,155))
        draw.text(text_pos, char, fill=text_color,font=font)
        text_pos = (text_pos[0] + font_size + 2,random.randint(7,15))

    
    del draw # I'm done drawing so I don't need this anymore
    
    # get the user session to save the captcha
    session = UserSession.objects.get(session_key = request.session.session_key)

    session.captcha = text
    session.save()
    print(session)
    # We need an HttpResponse object with the correct mimetype
    response = HttpResponse(content_type="image/png")
    # now, we tell the image to save as a PNG to the 
    # provided file-like object
    im.save(response, "png")

    return response # and we're done!
