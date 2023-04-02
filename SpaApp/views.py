from django.shortcuts import HttpResponse, render

# Create your views here.
def htmlRender(request):
    context = {
        "var1": 10,
        "var2": 15
    }

    return render(request, "index.html", context)
def index(request):
    
    return render(request, "index.html")

def services(request):
    
    return render(request, "services.html")

def products(request):
    
    return render(request, "products.html")

def delivery_page(request):
    
    return render(request, "delivery_page.html")

def receptionist_page(request):
    
    return render(request, "receptionist_page.html")

def owner_page(request):
    
    return render(request, "owner_page.html")

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

