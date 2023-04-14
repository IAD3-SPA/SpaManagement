from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from .tokens import account_activation_token
from .models import Owner, Supplier, Accountant, Receptionist

User = get_user_model()

def create_new_user(form):
    """create new user by roles"""
    if form.cleaned_data.get("type") == User.Types.RECEPTIONIST:
        return Receptionist.objects.create_user(
            username=form.cleaned_data.get("username"),
            first_name=form.cleaned_data.get("first_name"),
            last_name=form.cleaned_data.get("last_name"),
            email=form.cleaned_data.get("email"),
            password=form.cleaned_data.get("password1")
        )
    if form.cleaned_data.get("type") == User.Types.ACCOUNTANT:
        return Accountant.objects.create_user(
            username=form.cleaned_data.get("username"),
            first_name=form.cleaned_data.get("first_name"),
            last_name=form.cleaned_data.get("last_name"),
            email=form.cleaned_data.get("email"),
            password=form.cleaned_data.get("password1")
        )
    if form.cleaned_data.get("type") == User.Types.SUPPLIER:
        return Supplier.objects.create_user(
            username=form.cleaned_data.get("username"),
            first_name=form.cleaned_data.get("first_name"),
            last_name=form.cleaned_data.get("last_name"),
            email=form.cleaned_data.get("email"),
            password=form.cleaned_data.get("password1")
        )


