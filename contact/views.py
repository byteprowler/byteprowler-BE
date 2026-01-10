from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings


@api_view(["POST"])
@permission_classes([AllowAny])
def send_contact_email(request):
    name = (request.data.get("name") or "").strip()
    email = (request.data.get("email") or "").strip()
    message = (request.data.get("message") or "").strip()

    if not name or not email or not message:
        return Response(
            {"ok": False, "error": "Name, email, and message are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    subject = f"New Contact Message from {name}"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
            fail_silently=False,
        )
        return Response({"ok": True, "message": "Message sent successfully!"})
    except Exception as e:
        return Response(
            {"ok": False, "error": "Failed to send message."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )