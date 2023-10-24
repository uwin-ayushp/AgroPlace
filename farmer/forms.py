from django import forms
from store.models import Category, Product  # Import the Category model

class AddProductForm(forms.ModelForm):
    product_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Product Name',
            'class': 'form-control',
        }),
        label='Product Name'
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={  # Use Textarea for a larger description field
            'placeholder': 'Enter Product Description',
            'class': 'form-control',
        }),
        label='Product Description'
    )

    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter Product Price',
            'class': 'form-control',
        }),
        label='Price'
    )

    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
        })
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        label='Category'
    )

    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter Product Quantity',
            'class': 'form-control',
        }),
        label='Quantity'
    )

    is_available = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label='Available'
    )

    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'image', 'category', 'quantity', 'is_available']
