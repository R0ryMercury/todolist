from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from core.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True)

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
        password_repeat = attrs.pop("password_repeat", None)
        if password != password_repeat:
            raise ValidationError("passwords don't match")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        self.user = user
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError("username or password is incorrect")
        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ("id",)
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class UpdatePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )

    class Meta:
        model = User
        read_only_fields = ("id",)

    def validate(self, attrs):
        old_password = attrs.get("old_password")
        user = self.instance
        if not user.check_password(old_password):
            raise ValidationError({"old_password": "field is incorrect"})
        return attrs

    def update(self, instance: User, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save(update_fields=["password"])
        return instance
