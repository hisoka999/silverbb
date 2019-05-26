from django.forms import ModelForm

from cms.models import Page


class PageForm(ModelForm):
    class Meta:
        model = Page
        exclude = {}
