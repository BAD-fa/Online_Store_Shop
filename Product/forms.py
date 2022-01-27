from django import forms

from .models import ProductComment, Product


class CommentFrom(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'ایمیل شما'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام شما'}))

    class Meta:
        model = ProductComment
        fields = ['content', 'rate']

        widgets = {
            'content': forms.Textarea(attrs={'cols': 30, 'rows': 6, 'placeholder': "نظر خود را اینجا بنویسید..."}),
        }

    def save(self, *args, **kwargs):
        author = kwargs.pop('author')
        commit = kwargs.get('commit', True)
        product = kwargs.pop('product')
        self.instance.author = author
        self.instance.product = product
        return super().save(commit=commit)


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name']
