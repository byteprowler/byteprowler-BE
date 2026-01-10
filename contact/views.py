from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

from drf_spectacular.utils import extend_schema
from .serializers import ContactMessageSerializer

@extend_schema(
    request=ContactMessageSerializer,
    responses={200: dict, 400: dict, 500: dict},
)
@api_view(["POST"])
@permission_classes([AllowAny])
def send_contact_email(request):
    serializer = ContactMessageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {"ok": False, "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = serializer.validated_data

    name = data["name"]
    email = data["email"]
    message = data["message"]

    mode = data.get("mode", "individual")
    project_type = data.get("project_type", "")
    budget = data.get("budget", "")
    timeline = data.get("timeline", "")

    subject = f"New Contact Message from {name}"

    body_lines = [
        f"Name: {name}",
        f"Email: {email}",
        f"Mode: {mode}",
    ]

    if mode == "company":
        body_lines += [
            f"Project Type: {project_type}",
            f"Budget: {budget}",
            f"Timeline: {timeline}",
        ]

    body_lines += ["", "Message:", message]

    body = "\n".join(body_lines)

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
            fail_silently=False,
        )
        return Response({"ok": True, "message": "Message sent successfully!"})
    except Exception:
        return Response(
            {"ok": False, "error": "Failed to send message."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )