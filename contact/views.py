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
        # EVERYTHING below this must be indented by 4 spaces
        serializer = ContactSerializer(data=request.data)
        
        # This will now pass because your serializer has all the fields
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        sender_email = data.get('email')
        user_name = data.get('name', 'Anonymous')
        user_mode = data.get('mode', 'individual')
        
        subject = f"Inquiry from {user_name} ({user_mode})"
        
        body = f"""
        New message from: {user_name}
        Email: {sender_email}
        Mode: {user_mode}
        Project: {data.get('project_type', 'N/A')}
        Budget: {data.get('budget', 'N/A')}
        Timeline: {data.get('timeline', 'N/A')}
        
        Message:
        {data.get('message')}
        """

        try:
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.EMAIL_HOST_USER,
                to=[settings.CONTACT_RECEIVER_EMAIL],
                reply_to=[sender_email]
            )
            email.send(fail_silently=False)
            return Response({"message": "Mail successfully sent"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error sending email: {traceback.format_exc()}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)