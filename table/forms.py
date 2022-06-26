from django.forms import ModelForm
from .models import Order
from django import forms


class OrderForm(forms.Form):
    order_num = forms.CharField(max_length=50,
                                widget=forms.TextInput
                                (attrs={'id': 'order'}))
    price_usd = forms.CharField(max_length=50,
                                widget=forms.TextInput
                                (attrs={'id': 'usd',
                                        'onkeyup': 'usd2rub()',
                                        }))
    price_rub = forms.CharField(max_length=50,
                                widget=forms.TextInput
                                (attrs={'id': 'rub'}))
    delivery_time = forms.CharField(max_length=50,
                                    widget=forms.TextInput
                                    (attrs={'id': 'dt'}))

    # class Meta:
    #     model = Order
    #     fields = "__all__"
