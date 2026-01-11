from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    # These two are always sent by your React form
    email = serializers.EmailField()
    message = serializers.CharField()
    subject = serializers.CharField(required=False, allow_blank=True)
    
    # These might be missing from the payload, so we make them optional
    name = serializers.CharField(required=False, allow_blank=True, default="Anonymous")
    mode = serializers.CharField(required=False, allow_blank=True, default="individual")
    project_type = serializers.CharField(required=False, allow_blank=True, default="N/A")
    budget = serializers.CharField(required=False, allow_blank=True, default="N/A")
    timeline = serializers.CharField(required=False, allow_blank=True, default="N/A")