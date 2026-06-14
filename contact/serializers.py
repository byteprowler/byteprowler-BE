from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False, trim_whitespace=True)
    email = serializers.EmailField(required=True, allow_blank=False)
    subject = serializers.CharField(required=True, allow_blank=False, trim_whitespace=True)
    message = serializers.CharField(required=True, allow_blank=False, trim_whitespace=True)
