from django import forms

class AddProductForm(forms.Form):
    product_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Product Name',
        'class': 'form-control',

    }), label='Product Name')