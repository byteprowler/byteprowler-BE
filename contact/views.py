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
        message_html = linebreaks(escape(data["message"]))

        html_content = f"""
        <p><strong>New Byteprowler contact form message</strong></p>
        <p><strong>Name:</strong> {visitor_name}</p>
        <p><strong>Email:</strong> {escape(visitor_email)}</p>
        <p><strong>Subject:</strong> {escape(subject)}</p>
        <p><strong>Message:</strong></p>
        {message_html}
        """

        try:
            resend.Emails.send(
                {
                    "from": settings.DEFAULT_FROM_EMAIL,
                    "to": [settings.CONTACT_RECEIVER_EMAIL],
                    "subject": f"Byteprowler Contact: {subject}",
                    "html": html_content,
                    "reply_to": visitor_email,
                }
            )

            return Response(SUCCESS_RESPONSE, status=status.HTTP_200_OK)

        except Exception:
            logger.exception("Failed to send contact email.")
            return Response(EMAIL_ERROR_RESPONSE, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
