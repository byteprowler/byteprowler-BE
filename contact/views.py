import traceback
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import ContactSerializer

class ContactEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        sender_email = serializer.validated_data['email']
        subject = serializer.validated_data['subject']
        message = serializer.validated_data['message']

        try:
            email = EmailMessage(
                subject=f"New Inquiry: {subject}",
                body=f"From: {sender_email}\n\nMessage:\n{message}",
                from_email=settings.EMAIL_HOST_USER,
                to=["joshuaexcellency1@gmail.com"],
                reply_to=[sender_email]  
            )
            
            email.send(fail_silently=False)
            
            return Response(
                {"message": "Mail successfully sent! I will get back to you soon."}, 
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )