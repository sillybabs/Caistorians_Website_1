from urllib import request
from django import forms
from .models import Births_Deaths_and_Marriages



class Births_Deaths_and_MarriagesForm(forms.ModelForm):
    class Meta:
        model = Births_Deaths_and_Marriages
        fields = ['title', 'content', 'image', 'publication_date']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }