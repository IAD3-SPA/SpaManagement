import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode




from .utils import create_new_user, is_accountant, is_owner, is_owner_or_accountant, \
    is_owner_or_receptionist, is_owner_or_supplier, is_receptionist, is_supplier, \
    create_warning_message, order_product_by_name, is_cosmethologist, is_owner_or_cosmethologist
from .tokens import account_activation_token
from .models import ProductDelivery, Product, Client, Order,  Service, Appointment
from .forms import NewEmployeeForm, LoginForm, ProductDeliveryForm, ClientForm, ClientForm2, AppointmentClientForm, AppointmentForm


User = get_user_model()


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


def index(request):
    user = request.user

    if not user.is_authenticated:
        return render(request, "index.html")

    if is_owner(user):
        return render(request, "owner_page.html")
    elif is_supplier(user):
        return render(request, "delivery_page.html")
    elif is_accountant(user):
        return render(request, "accountant_page.html")
    elif is_receptionist(user):
        return render(request, "receptionist_page.html")
    else:
        return render(request, "index.html")


def services(request):
    return render(request, "services.html")


def products(request):
    return render(request, "products.html")


def schedule(request):
    # FIXME: Czemu byly dwie funkcje schedule
    role = request.user.type  # assuming that the user's role is stored in the 'type' field
    if role == 'OWNER':
        appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.filter(role=role)

    return render(request, 'schedule.html', {'appointments': appointments})


@login_required(login_url="login_user")
@user_passes_test(is_owner, login_url="index")
def owner_page(request):
    message = create_warning_message()
    return render(request, "owner_page.html", {'message': message})


@login_required(login_url="login_user")
@user_passes_test(is_owner_or_supplier, login_url="index")
def delivery_page(request):
    # FIXME: Czemy byly zdefiniowane dwie funkcjie delivery_page
    if request.method == 'POST':
        form = ProductDeliveryForm(request.POST)
        if form.is_valid():
            try:
                delivery_product = form.save()
                messages.success(request, f"Dodałeś {delivery_product.name} w ilości {delivery_product.amount}"
                                          f"do naszej bazy produktów!")

            except ValueError:
                messages.error(request, "Nie udało się dodać produktów. Nie oferujemy takiego produktu!")
            return redirect("delivery_page")
        messages.error(request, "Nie udało się dodać produktów")
    else:
        form = ProductDeliveryForm()
    context = {"form": form}
    return render(request, 'delivery_page.html', context)


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
                return redirect('owner_page')
            if is_accountant(user):
                return redirect('accountant_page')
            if is_receptionist(user):
                return redirect('receptionist_page')
            if is_supplier(user):
                return redirect('delivery_page')

            return render(request, 'index.html')

    form = LoginForm()
    clients = Client.objects.all()
    context = {"form": form , 'clients': clients}
    return render(request, "templates/login.html", context)


@login_required
@user_passes_test(is_owner)
def owner_page(request):
    return render(request, 'owner_page.html')


@login_required
@user_passes_test(is_accountant)
def accountant_page(request):
    return render(request, 'accountant_page.html')


@login_required
@user_passes_test(is_receptionist)
def receptionist_page(request):
    return render(request, 'receptionist_page.html')


@login_required
@user_passes_test(is_supplier)
def supplier_page(request):
    return render(request, 'delivery_page.html')


@login_required(login_url="login_user")
def logout_user(request):
    logout(request)
    return redirect("index")


def product_list(request):
    grouped_products = order_product_by_name(True)
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product = Product.objects.get(code=product_name)
        product.deficit_status = not product.deficit_status
        product.save()

    context = {'grouped_products': grouped_products.values()}
    return render(request, 'product_list.html', context)


@user_passes_test(is_owner_or_receptionist)
def products_store_page(request):
    grouped_products = order_product_by_name(False)
    clients = Client.objects.all()
    context = {'grouped_products': grouped_products.values(), 'clients': clients}
    return render(request, 'products_store_page.html', context)


@user_passes_test(is_owner_or_receptionist)
def delete_product(request, product_name, delivery_id):
    product_delivery = ProductDelivery.objects.get(name=product_name, delivery_id=delivery_id)
    product_delivery.amount -= 1
    product_delivery.save()
    return redirect('products_store_page')


def refund_product(request, product_name, client_id, order_id):
    product_delivery = ProductDelivery.objects.get(name=product_name)
    chosen_product = Product.objects.get(name=product_name)
    client = Client.objects.get(pk=client_id)
    client_orders = Order.objects.filter(client=client)
    single_order = client_orders.get(id=order_id)
    client.benefits_program -=  chosen_product.price
    product_delivery.amount += 1
    product_delivery.save()
    single_order.refunded = True
    single_order.save()
    return redirect('client_page', client_id=client.pk)


@user_passes_test(is_owner_or_receptionist)
def sell_product(request, product_name, delivery_id):
    product_delivery = ProductDelivery.objects.get(name=product_name, delivery_id=delivery_id)
    chosen_product = Product.objects.get(name=product_name)
    if request.method == 'POST':
        client_id = request.POST.get('client')
        if client_id:
            client = Client.objects.get(pk=client_id)
            order = Order.objects.create(product=chosen_product, client=client, date=datetime.date.today())
            product_delivery.amount -= 1
            product_delivery.save()
            return redirect('client_page', client_id=client.pk)
    else:
        return redirect('products_store_page')   
    



def change_deficit_status(request, product_name):
    product_delivery = Product.objects.get(name=product_name)
    product_delivery.deficit_status = not product_delivery.deficit_status
    product_delivery.save()
    return redirect('product_list')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except ObjectDoesNotExist:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("login_user")

    # error
    return redirect("index")


def appointment(request, primary_key):
    appointment_object = get_object_or_404(Appointment, pk=primary_key)
    if request.method == "POST":
        appointment_object.delete()
        return redirect("schedule")
    return render(request, 'appointment.html', {'appointment': appointment_object})


@user_passes_test(is_owner)
def client_register(request):
    if request.method == 'POST':
        form = ClientForm2(request.POST)
        if form.is_valid():
            client = form.save()
            return redirect(reverse('client_page', args=[client.id]))
    else:
        form = ClientForm2()
    return render(request, 'client_register.html', {'form': form})


@user_passes_test(is_owner)
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})


def client_page(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    orders = Order.objects.filter(client=client)
    grouped_products = order_product_by_name(False)
    context = {'grouped_products': grouped_products.values(), 'client': client, 'orders' : orders}
    return render(request, 'client_page.html', context)

def loyal_page(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    grouped_products = order_product_by_name(False)
    context = {'grouped_products': grouped_products.values(), 'client': client,}
    return render(request, 'loyal_page.html', context)

def go_to_client(request):
    if request.method == 'POST':
        client_id = request.POST.get('client')
        if client_id:
            return redirect(reverse('client_page', args=[client_id]))

@login_required(login_url="login_user")
@user_passes_test(is_owner_or_receptionist, login_url="index")
def new_appointment(request):
    if request.method == "POST":
        form = AppointmentClientForm(request.POST)
        if not form.is_valid():
            messages.warning(request, "Data spotania nie może być wcześniejsza niż pół godziny od teraz.")
            return redirect("new_appointment")
        appointment_object = form["appointment"].save(commit=False)
        appointment_object.employee = User.objects.get(id=form["appointment"].cleaned_data.get("employee"))
        if not None in form["client"].cleaned_data.values():
            client = form["client"].save()
            appointment_object.client = client
        print(appointment_object.employee.type)
        appointment_object.role = appointment_object.employee.type
        appointment_object.save()
        messages.success(request, "Dodano nowe spotkanie")
        if is_receptionist(request.user):
            return redirect("receptionist_page")
        if is_owner(request.user):
            return redirect("owner_page")
        return HttpResponseNotFound("Kim jesteś?")
    form = AppointmentClientForm()
    context = {"form": form}
    return render(request, 'new_appointment.html', context)


@login_required(login_url="login_user")
@user_passes_test(is_owner_or_receptionist, login_url="index")
def update_appointment(request, appointment_id):
    appointment_object = get_object_or_404(Appointment, pk=appointment_id)

    form = AppointmentForm(request.POST or None, instance=appointment_object)
    if request.method == "POST":

        if not form.is_valid():
            print(form.cleaned_data)
            messages.warning(request, "Nie udało się aktualizować spotkania!!")
            return redirect("update_appointment", appointment_id=appointment_id)
        form.save(commit=False)
        appointment_object.role = User.objects.get(id=form.cleaned_data.get("employee")).type
        form.save()
        messages.success(request, "Zmieniono termin wizyty")
        return redirect("schedule")

    context = {
        "form": form,
        "appointment": appointment_object,
    }

    return render(request, "update_appointment.html", context)


def service_list(request):
    list_services = Service.objects.all().order_by('service_name')
    grouped_services = {}
    for service in list_services:
        grouped_services[service.service_name] = {
            'name': service.service_name,
            'price': service.price,
            'description': service.description,
            'image': service.image,
            'service_status': service.service_status
        }

    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        service = Service.objects.get(code=service_name)
        service.service_status = not service.service_status
        service.save()

    context = {'grouped_services': grouped_services.values()}
    return render(request, 'services.html', context)


def change_service_status(request, service_name):
    service = Service.objects.get(service_name=service_name)
    service.service_status = not service.service_status
    service.save()
    return redirect('services')
