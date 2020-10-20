from django import forms
from django.core.validators import MinValueValidator
from .models import CATEGORY_CHOICES, DEFAULT_CATEGORY, Product


# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100, required=True, label='Наименование')
#     description = forms.CharField(max_length=2000, required=False, label="Описание",
#                            widget=forms.Textarea)
#     category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True, label='Категория',
#                                initial=DEFAULT_CATEGORY)
#     amount = forms.IntegerField(required=True, label='Остаток',validators=(MinValueValidator(0),))
#     price = forms.DecimalField(required=True,max_digits=7, label='Цена', decimal_places=2,
#                                 validators=(MinValueValidator(0),))

from django import forms
from webapp.models import Product, Cart, Order


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []


class CartAddForm(forms.ModelForm):
    class Meta:
        model = Cart
        # fields = []
        fields = ['qty']  # бонус


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['products']