from django.forms import ModelForm
from .models import News

class NewsForm(ModelForm):
    
    class Meta:
        model = News
        exclude = ['salesman']
        fields = [
            'title', 
            'body', 
            'publish_date', 
            'validityـduration', 
            'img', 
            'validityـduration',
            ]

        
