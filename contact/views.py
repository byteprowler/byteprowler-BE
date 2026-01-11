import traceback
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import ContactSerializer

class ContactEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        email_body = f"""
        New message from: {data.get('name')}
        Mode: {data.get('mode')}
        Email: {data.get('email')}
        
        Project Details:
        - Type: {data.get('project_type')}
        - Budget: {data.get('budget')}
        - Timeline: {data.get('timeline')}
        
        Message:
        {data.get('message')}
        """

        try:
            email = EmailMessage(
                subject=data.get('subject', 'New Inquiry'),
                body=email_body,
                from_email=settings.EMAIL_HOST_USER,
                to=[settings.CONTACT_RECEIVER_EMAIL],
                reply_to=[data.get('email')]
            )
            email.send(fail_silently=False)
            return Response({"message": "Message delivered ✅ I’ll reply soon!"}, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"EMAIL ERROR: {traceback.format_exc()}")
            return Response({"error": "Failed to send email. Check server logs."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)