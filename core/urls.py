from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from contact.views import ContactEmailView

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("api/contact/send/", ContactEmailView.as_view(), name="contact-send"),
    path("swagger/", SpectacularAPIView.as_view(), name="schema"),
    path("redocs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]