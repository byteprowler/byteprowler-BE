from django.urls import path
from .views import SendContactEmailAPIView

urlpatterns = [
    path("send/", SendContactEmailAPIView.as_view(), name="send_contact_email"),
]