from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    email = serializers.EmailField()
    message = serializers.CharField()
    name = serializers.CharField(required=False, allow_blank=True)
    subject = serializers.CharField(required=False, allow_blank=True)
    mode = serializers.CharField(required=False, allow_blank=True)
    project_type = serializers.CharField(required=False, allow_blank=True)
    budget = serializers.CharField(required=False, allow_blank=True)
    timeline = serializers.CharField(required=False, allow_blank=True)