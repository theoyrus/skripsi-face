from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers


# Membuat custom response dari serializer yg ada
class BaseModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.context:
            self._context = getattr(self.Meta, "context", {})
        try:
            self.is_data = self.context["is_data"]
        except KeyError:
            self.is_data = True

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if not self.is_data:
            return rep
        elif self.context["view"].action in ["create", "retrieve", "update", "destroy"]:
            return {"data": rep}
        elif self.context["request"].method in ["GET"] and self.context[
            "view"
        ].action not in ["list"]:
            return {"data": rep}
        return rep


class BaseHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.context:
            self._context = getattr(self.Meta, "context", {})
        try:
            self.is_data = self.context["is_data"]
        except KeyError:
            self.is_data = True

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if not self.is_data:
            return rep
        elif self.context["view"].action in ["create", "retrieve", "update", "destroy"]:
            return {"data": rep}
        return rep


User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "password")
        # extra_kwargs = {"password": {"write_only": True}}

    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
        return user

    # def perform_create(self, validated_data):
    #     return super().perform_create(validated_data)

    # def create(self, validated_data):
    #     user = User(
    #         email=validated_data["email"],
    #         username=validated_data["username"],
    #         first_name=validated_data["first_name"],
    #         last_name=validated_data["last_name"],
    #         full_name=f'{validated_data["first_name"]} {validated_data["last_name"]}',
    #         groups=validated_data["groups"],
    #     )
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user
