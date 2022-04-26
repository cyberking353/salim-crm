from . views import *
from django.urls import path
#password reset views
from django.contrib.auth import views as auth_views 
urlpatterns = [


    path('',homePage, name='home'),
    path('product/',productview, name='product'),
    path('customer/<str:pk>/',customer, name ='customer'),
    path('create_order/<str:pk>',createOrder, name='create_order'),
    path('update_order/<str:pk>/',updateOrder, name='update_order'),
    path('create_customer/',createCustomer, name='create_customer'),
    path('delete_order/<str:pk>/',deleteOrder,name='delete_order'),
    path('customer/update/<str:pk>/',updateCustomer, name='update_customer'),
    path('accounts/signup',signUp,name='signup'),
    path('accounts/login',loginPage,name='login'),
    path('accounts/logout',logoutPage,name='logout'),
    path('user/',userPage,name='user_page'),
    path('accounts/settings',accountSettings, name='account_settings'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
     name='reset_password'),

    path('password_reset_sent/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'),
     name='password_reset_confirm'),
    
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),
     name='password_reset_complete'),


]