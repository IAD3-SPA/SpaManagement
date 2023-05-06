from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
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
    is_owner_or_receptionist, is_owner_or_supplier, is_receptionist, is_supplier, create_warning_message, _order_product_by_name
from .tokens import account_activation_token
from .models import ProductDelivery, Product, Appointment
from .forms import NewEmployeeForm, LoginForm, ProductDeliveryForm, AppointmentClientForm, AppointmentForm


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
    message = create_warning_message()
    return render(request, "owner_page.html", {'message': message})


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
                return render(request, 'owner_page.html')
            elif is_accountant(user):
                return render(request, 'accountant_page.html')
            elif is_receptionist(user):
                return render(request, 'receptionist_page.html')
            elif is_supplier(user):
                return render(request, 'delivery_page.html')
            return render(request, 'index.html')
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
    grouped_products = _order_product_by_name(True)
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product = Product.objects.get(code=product_name)
        product.deficit_status = not product.deficit_status 
        product.save() 
           
    context = {'grouped_products': grouped_products.values()}
    return render(request, 'product_list.html', context)


def products_store_page(request):
    grouped_products = _order_product_by_name(False)
    context = {'grouped_products': grouped_products.values()}
    return render(request, 'products_store_page.html', context)


def delete_product(request, product_name, delivery_id):
    product_delivery = ProductDelivery.objects.get(name=product_name, delivery_id=delivery_id)
    product_delivery.amount -= 1
    product_delivery.save()
    return redirect('products_store_page')


def change_deficit_status(request, product_name):
    product_delivery = Product.objects.get(name=product_name)
    product_delivery.deficit_status = not product_delivery.deficit_status
    product_delivery.save()
    return redirect('product_list')


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

def schedule(request):
    role = request.user.type  # assuming that the user's role is stored in the 'type' field
    if role == 'OWNER':
        appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.filter(role=role)

    return render(request, 'schedule.html', {'appointments': appointments})

def appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        appointment.delete()
        return redirect("schedule")
    return render(request, 'appointment.html', {'appointment': appointment})

@login_required(login_url="login_user")
@user_passes_test(is_owner_or_receptionist, login_url="index")
def new_appointment(request):

    if request.method == "POST":
        form = AppointmentClientForm(request.POST)
        if not form.is_valid():
            messages.warning(request, "Data spotania nie może być wcześniejsza niż pół godziny od teraz.")
            return redirect("new_appointment")
        appointment = form["appointment"].save(commit=False)
        appointment.employee = User.objects.get(id=form["appointment"].cleaned_data.get("employee"))
        if not None in form["client"].cleaned_data.values():
            client = form["client"].save()
            appointment.client = client
        print(appointment.employee.type)
        appointment.role = appointment.employee.type
        appointment.save()
        messages.success(request, "Dodano nowe spotkanie")
        if is_receptionist(request.user):
            return redirect("receptionist_page") 
        elif is_owner(request.user):
            return redirect("owner_page")
        else:
            return HttpResponseNotFound("Kim jesteś?")
    form = AppointmentClientForm()
    context = {"form": form}
    return render(request, 'new_appointment.html', context)

@login_required(login_url="login_user")
@user_passes_test(is_owner_or_receptionist, login_url="index")
def update_appointment(request, appointment_id):

    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    form = AppointmentForm(request.POST or None, instance=appointment)
    if request.method == "POST":

        if not form.is_valid():
            print(form.cleaned_data)
            messages.warning(request, "Nie udało się aktualizować spotkania!!")
            return redirect("update_appointment", appointment_id=appointment_id)
        form.save(commit=False)
        appointment.role = User.objects.get(id=form.cleaned_data.get("employee")).type
        form.save()
        messages.success(request, "Zmieniono termin wizyty")
        return redirect("schedule")
    
    context = {
        "form": form,
        "appointment": appointment,
    }

    return render(request, "update_appointment.html", context)
