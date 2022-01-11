from django import forms

from .models import ProductComment


class CommentFrom(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = ProductComment
        fields = ['content', 'rate']

    def save(self, *args, **kwargs):
        user = kwargs.pop('user')
        commit = kwargs.get('commit', True)
        product = kwargs.pop('product')
        self.instance.author = user
        self.instance.product = product
        return super().save(commit=commit)
