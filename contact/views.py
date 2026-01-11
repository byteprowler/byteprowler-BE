import resend
import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import ContactSerializer

# Initialize Resend
resend.api_key = os.getenv("RESEND_API_KEY")

class ContactEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        
        # If frontend sends "name" or "budget", serializer now accepts them
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        html_content = f"""
        <strong>New Inquiry from {data.get('name')}</strong><br/>
        <strong>Email:</strong> {data.get('email')}<br/>
        <strong>Mode:</strong> {data.get('mode')}<br/>
        <p><strong>Message:</strong> {data.get('message')}</p>
        """

        try:
            resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": settings.CONTACT_RECEIVER_EMAIL,
                "subject": data.get('subject', 'New Inquiry'),
                "html": html_content,
                "reply_to": data.get('email')
            })
            
            return Response({"message": "Sent via API! Render can't block this! 🚀"}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)