
from .models import Category
from django import forms
from django.core.exceptions import ValidationError



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','offer_percentage']
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and name.strip() == '':
            raise ValidationError('Name cannot be only spaces')
        if Category.objects.filter(name=name).exists():
            raise ValidationError('A category with this name already exists')
        return name
