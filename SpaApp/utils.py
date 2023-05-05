from typing import Dict, List, Tuple, Union
from datetime import timedelta, date

from django.contrib.auth import get_user_model

from .models import Supplier, Accountant, Receptionist, Storage, Product, ProductDelivery

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
    if form.cleaned_data.get("type") == User.Types.COSMETHOLOGIST:
        return Supplier.objects.create_user(
            username=form.cleaned_data.get("username"),
            first_name=form.cleaned_data.get("first_name"),
            last_name=form.cleaned_data.get("last_name"),
            email=form.cleaned_data.get("email"),
            password=form.cleaned_data.get("password1")
        )


def is_owner(user):
    return user.type == User.Types.OWNER


def is_receptionist(user):
    return user.type == User.Types.RECEPTIONIST


def is_accountant(user):
    return user.type == User.Types.ACCOUNTANT


def is_supplier(user):
    return user.type == User.Types.SUPPLIER


def is_owner_or_receptionist(user):
    return is_owner(user) or is_receptionist(user)


def is_owner_or_accountant(user):
    return is_owner(user) or is_accountant(user)


def is_owner_or_supplier(user):
    return is_owner(user) or is_supplier(user)


def create_warning_message() -> Union[str, None]:
    """Creates a full warning massage with bullet points of expired and soon to be expired products"""
    message = None

    products_week_left = _create_full_storage_message(7, 0)
    products_expired = _create_full_storage_message(0)

    if any([products_expired, products_week_left]):
        message = "Warning!\n"
    else:
        return message

    if products_expired:
        message += f"Following products have expired:\n{products_expired}"

    if products_week_left:
        message += f"Following products have less than a week:\n{products_week_left}"

    return message


def _create_full_storage_message(days_top, days_bottom=None) -> Union[str, None]:
    """Creates message with bullet points of expired and soon to be expired products """
    storages = Storage

    expired_products = _get_expired_products(storages, days_top, days_bottom)

    message = _create_expired_product_message(expired_products)

    return message


def _get_expired_products(storages, days_top, days_bottom) -> List[Tuple[str, timedelta]]:
    """Returns a list of tuples of expired products and days left"""
    expired_products = []

    for storage in storages.objects.all():
        product = storage.product
        delivery = storage.delivery
        is_expired, time_left = _check_expiry_date(product, delivery, days_top, days_bottom)

        if is_expired:
            expired_products += [(product.name, time_left.days)]

    return expired_products


def _create_expired_product_message(expired_products) -> Union[str, None]:
    """Creates a bullet points list of product names and days left"""
    message = None

    if len(expired_products) <= 0:
        return message
    else:
        message = ''

    for name, days_left in expired_products:
        message += f"- {name}, {days_left} days\n"

    return message


def _check_expiry_date(product, delivery, days_top, days_bottom) -> Tuple[bool, timedelta]:
    """Checks whether product expired and returns boolean value and time left"""
    expiry_date = delivery.date + product.expiry_duration
    time_left = expiry_date - date.today()

    if days_bottom is not None:
        is_expired = timedelta(days=days_top) >= time_left > timedelta(days=days_bottom)
    else:
        is_expired = timedelta(days=days_top) >= time_left

    return is_expired, time_left


def _order_product_by_name(defifit_booelan) -> Dict[str, any]:
    products_list = ProductDelivery.objects.all().order_by('name')
    products_store = Product.objects.all().order_by('name')
    grouped_products = {}
    for product in products_list:
        if product.name in grouped_products:
            grouped_products[product.name]['total_amount'] += product.amount
        else:
            if defifit_booelan:
                grouped_products[product.name] = {
                    'name': product.name,
                    'total_amount': product.amount,
                    'image': products_store.get(name=product.name).image,
                    'deficit': products_store.get(name=product.name).deficit_status
                }
            else:
                grouped_products[product.name] = {
                    'name': product.name,
                    'total_amount': product.amount,
                    'image': products_store.get(name=product.name).image,
                    'price': products_store.get(name=product.name).price,
                    'delivery_id': product.delivery_id
            }
    return grouped_products