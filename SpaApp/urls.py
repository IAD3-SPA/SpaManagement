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
    path('product_list/', views.product_list, name='product_list'),
    path('change_deficit_status/<str:product_name>/', views.change_deficit_status, name='change_deficit_status'),
    path('products_store_page/', views.products_store_page, name='products_store_page'),
    path('delete_product/<str:product_name>/<int:delivery_id>/', views.delete_product, name='delete_product'),
    path('help/', views.help, name='help'),
    path('schedule/', views.schedule, name="schedule"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('appointment/<int:pk>/', views.appointment, name='appointment'),
    path('new_appointment/', views.new_appointment, name='new_appointment'),
    path('update_appointment/<int:appointment_id>', views.update_appointment, name='update_appointment'),
    
 
]