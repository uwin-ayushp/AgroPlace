from django import forms
from .models import ReviewRating

class ReviewForms(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject','review','rating']

class ProductSortForm(forms.Form):
    SORT_CHOICES = [
        ('new', 'New'),
        ('price_low_to_high', 'Price: Low to High'),
        ('price_high_to_low', 'Price: High to Low'),
    ]

    sort = forms.ChoiceField(choices=SORT_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select form-select-sm', 'id': 'sortOptions'}), label='')

class CatSortForm(forms.Form):
    CAT_CHOICES = [
        ('allproducts', 'Allproduct'),
        ('fruits', 'Fruits'),
        ('grains', 'Grains'),
        ('seeds', 'Seeds'),
        ('vegetable', 'Vegetable'),
    ]

    csort = forms.ChoiceField(choices=CAT_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select form-select-sm', 'id': 'catOptions'}), label='')