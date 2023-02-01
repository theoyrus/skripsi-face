from django.contrib.auth import get_user_model, models

from rest_framework import serializers

from apps.main.serializers import BaseHyperlinkedModelSerializer, BaseModelSerializer

User = get_user_model()
Group = models.Group
Permission = models.Permission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            "id",
            "name",
            "codename",
        )


class GroupSerializer(BaseHyperlinkedModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ["url", "id", "name", "permissions"]


class GroupListSerializer(BaseHyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "id", "name"]


class GroupCreateSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permissions_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Permission.objects.all(),
    )

    class Meta:
        model = Group
        fields = ("id", "name", "permissions", "permissions_ids")

    def create(self, validated_data):
        permissions_ids = validated_data.pop("permissions_ids")
        group = Group.objects.create(**validated_data)
        group.permissions.set(permissions_ids)
        return group

    def update(self, instance, validated_data):
        permissions_ids = validated_data.pop("permissions_ids")
        instance.permissions.set(permissions_ids)
        return super().update(instance, validated_data)


class UserSerializer(BaseHyperlinkedModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    # groups = GroupListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "groups",
        ]

        # extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            full_name=f'{validated_data["first_name"]} {validated_data["last_name"]}',
        )
        # user.
        user.set_password(validated_data["password"])
        # group = Group()
        # group.set_
        user.save()
        return user


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    # group = serializers.PrimaryKeyRelatedField(
    #     queryset=Group.objects.all(), required=False
    # )

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "password", "groups")
        extra_kwargs = {"passwords": {"write_only": True}}

    def create(self, validated_data):
        group = validated_data.pop("group", None)
        full_name = f"{validated_data['first_name']} {validated_data['last_name']}"
        validated_data["full_name"] = full_name
        user = User.objects.create(
            **validated_data,
        )
        user.set_password(validated_data["password"])
        user.save()
        if group:
            user.groups.add(group)
        return user
