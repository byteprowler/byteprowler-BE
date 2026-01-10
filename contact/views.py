from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .serializers import ContactSerializer

class ContactEmailView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Format the email body
            subject = f"Portfolio Inquiry from {data['name']} ({data['mode']})"
            
            message_body = f"""
            New message from: {data['name']}
            Reply-to: {data['email']}
            Category: {data['mode']}
            
            --- Project Details ---
            Type: {data.get('project_type', 'N/A')}
            Budget: {data.get('budget', 'N/A')}
            Timeline: {data.get('timeline', 'N/A')}
            
            --- Message ---
            {data['message']}
            """

            try:
                send_mail(
                    subject,
                    message_body,
                    settings.EMAIL_HOST_USER,
                    [settings.CONTACT_RECEIVER_EMAIL],
                    fail_silently=False,
                    reply_to=[data['email']],
                )
                return Response(
                    {"message": "Message delivered ✅ I’ll reply soon!"}, 
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"error": "Email server error. Please try again later."}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)