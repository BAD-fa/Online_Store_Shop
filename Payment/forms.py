from django import forms

from Payment.models import Wallet


class WalletUpdateForm(forms.Form):
        
    amount = forms.IntegerField()


class WalletCreationForm(forms.ModelForm):



    class Meta:
        model = Wallet
        fields = ["name"]
