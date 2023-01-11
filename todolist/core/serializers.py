from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[])
    password_repeat = serializers.CharField()

    class Meta:
        model = User
        read_only_fields = ("id",)
        fields = (
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "password_repeat",
        )

    def validate(self, attrs):
        password = attrs.get("password")
        password_repeat = attrs.pop("password", None)
        if password != password_repeat:
            raise ValidationError("passwords don't match")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        self.user = user
        return user