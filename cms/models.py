from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings 
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group

fs = FileSystemStorage(location=settings.STATICFILES_DIRS[0],base_url='/static/')
fs_data = FileSystemStorage(location='/home/stefan/workspace/silverbb/cms_data/',base_url='/cms/data/')    

class Gallery(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self',null=True,blank=True)
    show   = models.BooleanField(default=True)

    def get_url_name(self):
        return self.name.replace(' ','_')

    def __unicode__(self):
        return self.name

class Image(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cms_images',storage=fs)
    thumb = models.ImageField(upload_to='cms_thumbs',storage=fs,blank=True,null=True)
    gallery = models.ForeignKey(Gallery)
    
    def __unicode__(self):
        return self.name
    
    def create_thumbnail(self):
        # original code for this method came from
        # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/
        
        # If there is no image associated with this.
        # do not create thumbnail
        if not self.image:
            return
        
        import PIL
        from cStringIO import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os
        
        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (200,200)
        
        DJANGO_TYPE = self.image.file.content_type
        
        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
        
        # Open original photo which we want to thumbnail using PIL's Image
        image = PIL.Image.open(StringIO(self.image.read()))
        
        # Convert to RGB if necessary
        # Thanks to Limodou on DjangoSnippets.org
        # http://www.djangosnippets.org/snippets/20/
        #
        # I commented this part since it messes up my png files
        #
        #if image.mode not in ('L', 'RGB'):
        #    image = image.convert('RGB')
        
        # We use our PIL Image object to create the thumbnail, which already
        # has a thumbnail() convenience method that contrains proportions.
        # Additionally, we use Image.ANTIALIAS to make the image look better.
        # Without antialiasing the image pattern artifacts may result.
        image.thumbnail(THUMBNAIL_SIZE, PIL.Image.ANTIALIAS)
        
        # Save the thumbnail
        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)
        
        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                temp_handle.read(), content_type=DJANGO_TYPE)
        # Save SimpleUploadedFile into image field
        self.thumb.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)
 
    def save(self):
        # create a thumbnail
        self.create_thumbnail()
        
        super(Image, self).save()

class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=True,blank=True)
    gallery = models.ForeignKey(Gallery,null=True,blank=True)
    
    def __unicode__(self):
        return self.title
    
    def get_url_name(self):
        return self.title.replace(' ','_')

class Topic(models.Model):
    title = models.CharField(max_length=100)
    pages = models.ManyToManyField(Page)
    
    
    def __unicode__(self):
        return self.title
    

class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    external_link = models.URLField(null=True,blank=True)
    topic = models.ForeignKey(Topic,null=True,blank=True)
    module = models.CharField(max_length=150,null=True,blank=True)
    parent = models.ForeignKey('self',null=True,blank=True)

    def module_path(self):
        return reverse(self.module)
    
    def get_url_name(self):
        return self.title.replace(' ','_')
    
    def __unicode__(self):
        return self.title
    
class NewsItem(models.Model):
    title = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)
    content = models.TextField()
    
    def __unicode__(self):
        return self.title
    
class DownloadCategory(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self',null=True,blank=True)
    visible = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name
    
class Download(models.Model):
    name = models.CharField(max_length=150)
    data = models.FileField(upload_to='cms_data',storage=fs_data)
    mime_type = models.CharField(max_length = 30,null=True,blank=True) 
    size = models.IntegerField(default = 0)
    group = models.ForeignKey(Group,null=True,blank=True)
    descrption = models.TextField()
    visible = models.BooleanField()
    count = models.IntegerField(default=0)
    category = models.ForeignKey(DownloadCategory)


    def get_type(self):
        return self.mime_type.replace('/','-x-')
    def save_data(self):
        if not self.data:
            return
        
        self.mime_type = self.data.file.content_type
        self.size = self.data.file._size
        #self.size = self.data.file.
 
    def save(self):
        # create a thumbnail
        self.save_data()
        
        super(Download, self).save()