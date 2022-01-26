from django import forms

class WalletForm(forms.Form):
        
    amount = forms.IntegerField()
