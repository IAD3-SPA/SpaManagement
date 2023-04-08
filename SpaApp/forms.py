from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth import authenticate, get_user_model
from .models import ProductDelivery
from django.forms import DateInput


class NewEmployeeForm(UserCreationForm):
    
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update(self.forms_attrs("Imie"))
        self.fields["last_name"].widget.attrs.update(self.forms_attrs("Nazwisko"))
        self.fields["username"].widget.attrs.update(self.forms_attrs("Nazwa użytkownika"))
        self.fields["email"].widget.attrs.update(self.forms_attrs("Email"))
        self.fields["password1"].widget.attrs.update(self.forms_attrs("Hasło"))
        self.fields["password2"].widget.attrs.update(self.forms_attrs("Powtórz hasło"))

    def forms_attrs(self, placeholder):
        return {
            "class": "form-control my-3",
            "placeholder": placeholder,
            }

    def save(self, commit=True):
        user = super(NewEmployeeForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(forms.Form, NewEmployeeForm):

    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(self.forms_attrs("Email"))
        self.fields["password"].widget.attrs.update(self.forms_attrs("Password"))


class ProductDeliveryForm(forms.ModelForm):
    class Meta:
        model = ProductDelivery
        fields = ['name', 'amount', 'date']
        widgets = {
                'date': DateInput( attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                })
        }