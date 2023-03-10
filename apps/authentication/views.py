# from django.shortcuts import render
from rest_framework import permissions, viewsets, filters

from .serializers import (
    Group,
    GroupCreateSerializer,
    GroupListSerializer,
    GroupSerializer,
    User,
    UserCreateSerializer,
    UserSerializer,
)


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk mengelola user
    """

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return UserCreateSerializer
        return UserSerializer

    queryset = User.objects.all()
    # serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "email", "full_name"]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk mengelola group
    """

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            # jika proses create/update, pakai serializer yg berbeda
            return GroupCreateSerializer
        # elif self.action in ["list"]:
        #     # jika proses list, pakai serializer non permission
        #     return GroupListSerializer
        return GroupSerializer

    queryset = Group.objects.all()
    # serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]
