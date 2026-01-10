from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    message = serializers.CharField()
    mode = serializers.ChoiceField(choices=["individual", "company"])
    # Optional fields (match your React payload keys)
    project_type = serializers.CharField(required=False, allow_blank=True)
    budget = serializers.CharField(required=False, allow_blank=True)
    timeline = serializers.CharField(required=False, allow_blank=True)