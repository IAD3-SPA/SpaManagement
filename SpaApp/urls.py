from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.products, name='products'),    
    path('receptionist_page/', views.receptionist_page, name='receptionist_page'),     
    path('owner_page/', views.owner_page, name='owner_page'),           
    path('delivery_page/', views.delivery_page, name='delivery_page'),
    path('accountant_page/', views.accountant_page, name='accountant_page'),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_user, name="logout_user"),
    path('login/', views.login_user, name="login_user"),



    path('help/', views.help, name='help'),
    path('html/', views.htmlRender, name='htmlRender')
]