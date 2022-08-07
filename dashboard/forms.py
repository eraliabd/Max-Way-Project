from django import forms
from food.models import Category, Product, Customer

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.TextInput(attrs={'class': 'form-control'}),
            "price": forms.NumberInput(attrs={'class': 'form-control'}),
            "cost": forms.NumberInput(attrs={'class': 'form-control'}),
            "image": forms.FileInput(attrs={'class': 'form-control', 'onchange': 'loadFile(event)'}),
            "category": forms.Select(attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "phone_number": forms.NumberInput(attrs={'class': 'form-control'}),
        }