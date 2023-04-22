from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import DateInput
from django.contrib import messages
from bootstrap_datepicker_plus.widgets import DatePickerInput
from betterforms.multiform import MultiModelForm

from .models import ProductDelivery, Client, Appointment
from .utils import FormsAttr, get_next_hour
from datetime import datetime,date

user = get_user_model()


class NewEmployeeForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = user
        fields = ("first_name", "last_name", "username", "email", "password1", "password2", "type")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update(FormsAttr.forms_attrs("Imie"))
        self.fields["last_name"].widget.attrs.update(FormsAttr.forms_attrs("Nazwisko"))
        self.fields["username"].widget.attrs.update(FormsAttr.forms_attrs("Nazwa użytkownika"))
        self.fields["email"].widget.attrs.update(FormsAttr.forms_attrs("Email"))
        self.fields["password1"].widget.attrs.update(FormsAttr.forms_attrs("Hasło"))
        self.fields["password2"].widget.attrs.update(FormsAttr.forms_attrs("Powtórz hasło"))
        self.fields["type"].widget.attrs.update({"placeholder": "Type"})


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
        self.fields["email"].widget.attrs.update(FormsAttr.forms_attrs("Email"))
        self.fields["password"].widget.attrs.update(FormsAttr.forms_attrs("Password"))


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

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    description = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = Appointment
        fields = ["name", "description", "date", "time"]

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(FormsAttr.forms_attrs("Nazwa"))
        self.fields["description"].widget.attrs.update(FormsAttr.forms_attrs("Informacje dodatkowe..."))
        self.fields["date"].widget.attrs.update(FormsAttr.forms_attrs())
        self.fields["time"].widget.attrs.update(FormsAttr.forms_attrs())
        self.initial["time"] = get_next_hour()

    def clean(self):
        cleaned_data = super().clean()
        date = self.cleaned_data.get('date')
        time = self.cleaned_data.get('time')
        if date and time:
            print(type(date))
            if date < date.today() or time < datetime.now().time():
                raise forms.ValidationError("Podana data jest przeszła.")
        return cleaned_data



class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "surname", "phone_number"]
    
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(FormsAttr.forms_attrs("Imie"))
        self.fields["surname"].widget.attrs.update(FormsAttr.forms_attrs("Nazwisko"))
        self.fields["phone_number"].widget.attrs.update(FormsAttr.forms_attrs("+48..."))


class AppointmentClientForm(MultiModelForm):
    form_classes = {
        "client": ClientForm,
        "appointment": AppointmentForm
    }