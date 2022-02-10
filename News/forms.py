from django.forms import ModelForm

from User.models import Customer
from .models import News
from email.mime import image
from django import forms





class CreateNewsForm(forms.ModelForm):

    publish_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = News
        fields = ['title','content','publish_date','image','validityـduration','news_slug']


class AddSubscriberForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['email']

