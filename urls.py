from django.urls import path

from . import views

app_name = "django_esign"
urlpatterns = [
    path('webhook_hellosign/', views.webhook_hellosign, name="webhook_hellosign"),
]