from django import forms

class AddProduct(forms.Form):
    Name = forms.CharField(label='Name', max_length=100)
    Desc = forms.CharField(label='Description', max_length=500)
