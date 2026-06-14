from django.urls import path
from .views import ContactEmailView

urlpatterns = [
    path("send/", ContactEmailView.as_view(), name="send_contact_email"),
]
