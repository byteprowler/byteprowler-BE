from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    subject = serializers.CharField(max_length=250, required=True)
    message = serializers.CharField(max_length=2000, required=True)