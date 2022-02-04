from django.forms import ModelForm
from .models import News
from email.mime import image
from django import forms




# class NewsForm(ModelForm):
#     class Meta:
#         model = News
#         exclude = ['salesman']
#         fields = [
#             'title',
#             'body',
#             'publish_date',
#             'validityـduration',
#             'img',
#             'validityـduration',
#         ]



class CreateNewsForm(forms.ModelForm):
    publish_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    # image = forms.FileField()

    class Meta:
        model = News
        fields = ['title','content','publish_date','image','validityـduration','news_slug']

    # def save(self, commit: bool = ...):
    #     if CreateNewsForm.is_valid(self):
    #         if 'image' in self.cleaned_data.FILES:
    #             image = self.cleaned_data.FILES['image']
    #     return super().save(commit)
        
    