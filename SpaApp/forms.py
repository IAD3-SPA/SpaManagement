from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import ProductDelivery
from django.forms import DateInput
from django.core.validators import MinValueValidator

user = get_user_model()


class NewEmployeeForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = user
        fields = ("first_name", "last_name", "username", "email", "password1", "password2", "type")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update(self.forms_attrs("Imie"))
        self.fields["last_name"].widget.attrs.update(self.forms_attrs("Nazwisko"))
        self.fields["username"].widget.attrs.update(self.forms_attrs("Nazwa użytkownika"))
        self.fields["email"].widget.attrs.update(self.forms_attrs("Email"))
        self.fields["password1"].widget.attrs.update(self.forms_attrs("Hasło"))
        self.fields["password2"].widget.attrs.update(self.forms_attrs("Powtórz hasło"))
        self.fields["type"].widget.attrs.update({"placeholder": "Type"})

    @staticmethod
    def forms_attrs(placeholder):
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
            'date': DateInput(attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
            })
        }
        

        # validators = {
        #     'amount': [MinValueValidator(0)]
        # }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount < 0:
            raise forms.ValidationError("Ilość produktów musi być większa lub równa 0.")
        return amount