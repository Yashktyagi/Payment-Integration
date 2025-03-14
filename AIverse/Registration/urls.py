from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path("",views.registration_form, name="registration_form"),
    path("payment_success/", views.payment_success, name="payment_success"),

]
