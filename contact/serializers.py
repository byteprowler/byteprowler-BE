from rest_framework import serializers


class ContactMessageSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    message = serializers.CharField()

    # ✅ Optional extra fields (Option B)
    mode = serializers.ChoiceField(
        choices=[("individual", "individual"), ("company", "company")],
        required=False,
        default="individual",
    )
    project_type = serializers.CharField(required=False, allow_blank=True, max_length=120)
    budget = serializers.CharField(required=False, allow_blank=True, max_length=120)
    timeline = serializers.CharField(required=False, allow_blank=True, max_length=120)

    def validate(self, attrs):
        mode = attrs.get("mode", "individual")

        if mode == "company":
            missing = {}
            if not attrs.get("project_type"):
                missing["project_type"] = ["This field is required when mode is company."]
            if not attrs.get("budget"):
                missing["budget"] = ["This field is required when mode is company."]
            if not attrs.get("timeline"):
                missing["timeline"] = ["This field is required when mode is company."]

            if missing:
                raise serializers.ValidationError(missing)

        return attrs