from datetime import date, timedelta

from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from .utils import create_new_user, is_accountant, is_owner, is_owner_or_accountant, \
    is_owner_or_receptionist, is_owner_or_supplier, is_receptionist, is_supplier
from .tokens import account_activation_token
from .models import Storage


def send_registration_mail(request, user, email_to_send):
    template_context = {
        "user": user.first_name + " " + user.last_name,
        "domain": get_current_site(request).domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": account_activation_token.make_token(user),
        "Protocol": "https" if request.is_secure() else "http"
    }
    template = render_to_string('activate.html', template_context)
    mail_subject = "Aktywacja konta."
    email = EmailMessage(
        mail_subject,
        template,
        settings.EMAIL_HOST_USER,
        [email_to_send]
    )
    email.send()


User = get_user_model()

from .forms import NewEmployeeForm, LoginForm
from .forms import ProductDeliveryForm
from .models import ProductDelivery


def index(request):
    return render(request, "index.html")


def services(request):
    return render(request, "services.html")


def products(request):
    return render(request, "products.html")


def schedule(request):
    return render(request, "schedule.html")


@login_required(login_url="login_user")
@user_passes_test(is_owner, login_url="index")
def owner_page(request):
    message = _create_warning_message()
    return render(request, "owner_page.html", {'message': message})


def _create_warning_message():
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


def _create_full_storage_message(days_top, days_bottom=None):
    storages = Storage

    expired_products = _get_expired_products(storages, days_top, days_bottom)

    message = _create_expired_product_message(expired_products)

    return message


def _get_expired_products(storages, days_top, days_bottom):
    expired_products = []

    for storage in storages.objects.all():
        product = storage.product
        delivery = storage.delivery
        is_expired, time_left = _check_expiry_date(product, delivery, days_top, days_bottom)

        if is_expired:
            expired_products += [(product.name, time_left.days)]

    return expired_products


def _create_expired_product_message(expired_products):
    message = ''

    if len(expired_products) <= 0:
        return message

    for name, days_left in expired_products:
        message += f"- {name}, {days_left} days\n"

    return message


def _check_expiry_date(product, delivery, days_top, days_bottom):
    expiry_date = delivery.date + product.expiry_duration
    time_left = expiry_date - date.today()

    if days_bottom is not None:
        is_expired = timedelta(days=days_top) >= time_left > timedelta(days=days_bottom)
    else:
        is_expired = timedelta(days=days_top) >= time_left

    return is_expired, time_left


@login_required(login_url="login_user")
@user_passes_test(is_owner_or_supplier, login_url="index")
def delivery_page(request):
    return render(request, "delivery_page.html")


@login_required(login_url="login_user")
@user_passes_test(is_owner_or_receptionist, login_url="index")
def receptionist_page(request):
    return render(request, "receptionist_page.html")


@login_required(login_url="login_user")
@user_passes_test(is_owner_or_accountant, login_url="index")
def accountant_page(request):
    return render(request, "accountant_page.html")


def contact(request):
    return render(request, "strona_kotaktowa.html")


# widok do usunięcia
def help(request):
    text = """
    Naszym głównym katalogiem jest katalog SpaApp: <br>
    - w pliku urls.py dodajemy kolejne strony w naszej aplikacji według schematu: path('<scieżka url>', views.<nazwa funkcji>, 
                    i nazwa - proponuje nazywac od nazwy funkcji) <br>
    - plik views.py jest plikiem na widoki podstron, w nim tworzymy funkcjie (lub klasy) odpowiadające jednej stronie w naszej aplikacji,
                    na koniec zwracamy naszą strone. Do zwracania plikow HTML służy render - w pliku views jest przykład /html <br>
    - plik models.py przechowuje modele bazy danych, jedna klasa odpowiada jednej tabeli w bazie danych, jest tam przykładowa klasa i 
                    jeśli chcemy dodać ją do bazy danych musimy zrobić migracje (jak w Laravel)<br>
    - html dodajemy do katalogu templates, css do static/css, js do static/js, żeby style zadziałały na stronie trzeba je załadować tak jak w przykładzie
    i to chyba tyle
    """

    return HttpResponse(text)


def register(request):
    if request.method == "POST":
        form = NewEmployeeForm(request.POST)
        if form.is_valid():
            user = create_new_user(form)
            user.save()
            send_registration_mail(request, user, user.email)

            return redirect("index")

    form = NewEmployeeForm()
    context = {"form": form}
    return render(request, "templates/register.html", context)


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if is_owner(user):
                return redirect("owner_page")
            elif is_accountant(user):
                return redirect("accountant_page")
            elif is_receptionist(user):
                return redirect("recepiotnist_page")
            elif is_supplier(user):
                return redirect("delivery_page")
            return redirect("index")
        messages.error(request, "Nie udało się zalogować")
        return redirect("login_user")

    form = LoginForm()

    context = {"form": form}
    return render(request, "templates/login.html", context)


@login_required(login_url="login_user")
def logout_user(request):
    logout(request)
    return redirect("index")


def delivery_page(request):
    if request.method == 'POST':
        form = ProductDeliveryForm(request.POST)
        if form.is_valid():
            try:
                delivery_product = form.save()
                messages.success(request,
                                 "Dodałeś {} w ilości {} do naszej bazy produktów!".format(delivery_product.name,
                                                                                           delivery_product.amount))
            except ValueError as e:
                messages.error(request, "Nie udało się dodać produktów. Nie oferujemy takiego produktu!")
            return redirect("delivery_page")
        messages.error(request, "Nie udało się dodać produktów")
    else:
        form = ProductDeliveryForm()
    context = {"form": form}
    return render(request, 'delivery_page.html', context)


def product_list(request):
    products_list = ProductDelivery.objects.all().order_by('name')
    grouped_products = {}
    for product in products_list:
        if product.name in grouped_products:
            grouped_products[product.name]['total_amount'] += product.amount
        else:
            grouped_products[product.name] = {
                'name': product.name,
                'total_amount': product.amount
            }
    context = {'grouped_products': grouped_products.values()}
    return render(request, 'product_list.html', context)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    print(user)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # messages success
        return redirect("login_user")

    # error
    return redirect("index")
