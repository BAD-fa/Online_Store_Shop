from django import forms

from Payment.models import Wallet


class WalletUpdateForm(forms.Form):
        
    amount = forms.IntegerField()

