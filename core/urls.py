from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from contact.views import ContactEmailView
from core.views import HealthCheckView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("api/contact/send/", ContactEmailView.as_view(), name="contact-send"),
    path("swagger/", SpectacularAPIView.as_view(), name="schema"),
    path("redocs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
