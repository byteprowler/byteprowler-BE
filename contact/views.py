import logging

import resend
from django.conf import settings
from django.utils.html import escape, linebreaks
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ContactSerializer

logger = logging.getLogger(__name__)

SUCCESS_RESPONSE = {
    "success": True,
    "message": "Transmission secure. Message received.",
}

VALIDATION_ERROR_RESPONSE = {
    "success": False,
    "message": "Please provide all required fields.",
}

EMAIL_ERROR_RESPONSE = {
    "success": False,
    "message": "Message could not be sent. Please try again later.",
}

ACKNOWLEDGEMENT_SUBJECT = "Message received - Byteprowler"


class ContactEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ContactSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(VALIDATION_ERROR_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        if not all(
            [
                settings.RESEND_API_KEY,
                settings.DEFAULT_FROM_EMAIL,
                settings.CONTACT_RECEIVER_EMAIL,
            ]
        ):
            logger.error("Contact email configuration is incomplete.")
            return Response(EMAIL_ERROR_RESPONSE, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        resend.api_key = settings.RESEND_API_KEY

        visitor_name = escape(data["name"])
        visitor_email = data["email"]
        subject = data["subject"]

        try:
            resend.Emails.send(
                {
                    "from": settings.DEFAULT_FROM_EMAIL,
                    "to": [settings.CONTACT_RECEIVER_EMAIL],
                    "subject": f"Byteprowler Contact: {subject}",
                    "html": self._build_notification_html(
                        visitor_name=visitor_name,
                        visitor_email=visitor_email,
                        subject=subject,
                        message=data["message"],
                    ),
                    "reply_to": visitor_email,
                }
            )

            try:
                resend.Emails.send(
                    {
                        "from": settings.DEFAULT_FROM_EMAIL,
                        "to": [visitor_email],
                        "subject": ACKNOWLEDGEMENT_SUBJECT,
                        "html": self._build_acknowledgement_html(visitor_name),
                        "reply_to": settings.CONTACT_RECEIVER_EMAIL,
                    }
                )
            except Exception:
                logger.exception("Failed to send contact acknowledgement email.")

            return Response(SUCCESS_RESPONSE, status=status.HTTP_200_OK)

        except Exception:
            logger.exception("Failed to send contact email.")
            return Response(EMAIL_ERROR_RESPONSE, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _build_notification_html(self, visitor_name, visitor_email, subject, message):
        message_html = linebreaks(escape(message))

        return f"""
        <p><strong>New Byteprowler contact form message</strong></p>
        <p><strong>Name:</strong> {visitor_name}</p>
        <p><strong>Email:</strong> {escape(visitor_email)}</p>
        <p><strong>Subject:</strong> {escape(subject)}</p>
        <p><strong>Message:</strong></p>
        {message_html}
        """

    def _build_acknowledgement_html(self, visitor_name):
        return f"""
        <p>Hi {visitor_name},</p>
        <p>Thanks for reaching out to Byteprowler. Your message has been received securely.</p>
        <p>I will review it and get back to you as soon as possible.</p>
        <p>Best,<br/>Joshua</p>
        """
