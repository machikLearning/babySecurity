from .models import *
from django import forms
import secrets
import hashlib

class BabySickForm(forms.ModelForm):
    authentication = forms.CharField(max_length=50, required=True)
    class Meta:
        model = BabySick
        fields = ["authentication", "IsSick"]

    def clean_authentication(self):
        data = self.cleaned_data["authentication"]
        return data

    def clean_IsSick(self):
        data = self.cleaned_data["IsSick"]
        return data

class ProductionActiveForm(forms.Form):
    userId = forms.CharField(max_length=10,required=True)
    authentication = forms.CharField(max_length=50,required=True)

    def clean_authentication(self):
        data = self.cleaned_data["authentication"]
        return data

    def clean_userId(self):
        data = self.cleaned_data["userId"]
        return data


class CreationProductionForm(forms.ModelForm):
    offerId = forms.CharField(max_length=10,required=True)
    class Meta:
        model = Product
        fields = ( "offerId", "authentication" )

    def clean_offer(self):
        data = self.cleaned_data["offerId"]
        return data

    def clean_authentication(self):
        data = self.cleaned_data["authentication"]
        return data

class BabyPictureForm(forms.ModelForm):
    authentication = forms.CharField(max_length=50,required=True)
    class Meta:
        model = BabyPicture
        fields=["image","authentication"]

    def clean_image(self):
        data = self.cleaned_data["image"]
        return data

    def clean_authentication(self):
        data = self.cleaned_data["authentication"]
        return data


