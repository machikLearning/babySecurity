from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User




class CreateUserForm(UserCreationForm):
    productionKey = forms.IntegerField(required=True)
    productionKey.widget.attrs.update({'class' : 'form-control'})
    userId = forms.CharField(max_length=10)
    userId.widget.attrs.update({'class' : 'form-control'})
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = ("userId", "productionKey", "password1", "password2")

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.key = self.cleaned_data["userId"]
        user.productionKey = self.cleaned_data["productionKey"]
        if commit:
            user.save()
        return user

class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=10, required=True)
    username.widget.attrs.update({'class': 'form-control'})
    password = forms.CharField(label="password",widget=forms.PasswordInput())
    password.widget.attrs.update({'class' : 'form-control'})
    class Meta:
        model = User
        fields = ["username","password"]


    def clean_userId(self):
        userId = self.cleaned_data["username"]
        return userId

    def clean_password(self):
        password = self.cleaned_data["password"]
        return password
