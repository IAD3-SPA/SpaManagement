from django.urls import path

from . import views


handler404 = views.handler404


urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.service_list, name='services'),
    path('contact/', views.contact, name='contact'),
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
    path('sell_product/<str:product_name>/<int:delivery_id>/', views.sell_product, name='sell_product'),
    path('refund_product/<str:product_name>/<int:client_id>/<int:order_id>', views.refund_product, name='refund_product'),
    path('change_service_status/<str:service_name>/', views.change_service_status, name='change_service_status'), 
    path('schedule/', views.schedule, name="schedule"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('appointment/<int:pk>/', views.appointment, name='appointment'),
    path('client_register/', views.client_register, name="client_register"),
    path('client_list/', views.client_list, name="client_list"),
    path('clients/', views.client_list, name='client_list'),
    path('login/<int:client_id>/', views.client_page, name='client_page'),
    path('login/<int:client_id>/loyal/', views.loyal_page, name='loyal_page'),
    path('new_appointment/', views.new_appointment, name='new_appointment'),
    path('update_appointment/<int:appointment_id>', views.update_appointment, name='update_appointment'),
    path('404/', views.handler404, name='handler404'),
    ]

