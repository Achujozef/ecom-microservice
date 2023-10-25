import re
from django.core.exceptions import ValidationError
from django import forms
from .models import  Address
from django import forms

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["name","housename", "locality", "phone", "city", "state", "zipcode"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'housename': forms.TextInput(attrs={'class': 'form-control'}),
            "locality": forms.TextInput(attrs={'class': 'form-control'}),
            "city": forms.TextInput(attrs={'class': 'form-control'}),
            "state": forms.Select(attrs={'class': 'form-control'}),
            "zipcode": forms.NumberInput(attrs={'class': 'form-control'}),
            "phone": forms.TextInput(attrs={'class': 'form-control'}),

        }
        labels={
            'name':'Name',
            'housename':'House no.',
            'locality':'Locality',
            'city':'City',
            'state':'State',
            'zipcode':'Zipcode',
            'phone':'Phone',
        }
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(r'^\d{10}$', phone):
            raise ValidationError("Phone number must be entered in the format: '9999999999'")
        return phone

    def clean_zipcode(self):
        zipcode = self.cleaned_data['zipcode']
        if not re.match(r'^\d{6}$', str(zipcode)):
            raise ValidationError("Enter a valid zipcode.")
        return zipcode
