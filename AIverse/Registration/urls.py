from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path("",views.registration_form),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-webhook/", views.payment_webhook, name="payment_webhook"),
]
