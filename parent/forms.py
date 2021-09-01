
from .models import *
from django import forms
from django.db import models
from rasberrypy.models import Product

from .models import  UserToken


class CreateToken(forms.ModelForm):
    class Meta:
        model =UserToken
        fields = ("token",)

    def clean_token(self):
        data = self.cleaned_data["token"]
        return data



class ProductionConfigure(forms.ModelForm):
    timeConfigure = forms.IntegerField()
    mode = forms.BooleanField()
    timeConfigure.widget.attrs.update({'class' : 'form-control'})
    class Meta:
        model = Product
        fields= ("timeConfigure","mode")
    def clean_timeConfigure(self):
        data = self.cleaned_data["timeConfigure"]
        return data

    def clean_mode(self):
        data = self.cleaned_data["mode"]
        return data


