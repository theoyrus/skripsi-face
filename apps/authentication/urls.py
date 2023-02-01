from django.urls import re_path, include
from rest_framework_simplejwt import views
from .views import UserViewSet, GroupViewSet
from .token import AppTokenObtainPairView


# user_viewset = UserViewSet.as_view({"get": "list", "post": "create"})
# user_detail_viewset = UserViewSet.as_view({"get": "retrieve"})
# group_viewset = GroupViewSet.as_view({"get": "list", "post": "create"})
# group_detail_viewset = GroupViewSet.as_view({"get": "retrieve"})

from core.helpers import OptionalSlashRouter

# router = routers.DefaultRouter()
router = OptionalSlashRouter()
router.register(r"user", UserViewSet)
router.register(r"group", GroupViewSet)


urlpatterns = [
    re_path(r"", include(router.urls)),
    re_path(r"login", AppTokenObtainPairView.as_view(), name="auth-login"),
    re_path(r"refresh", views.TokenRefreshView.as_view(), name="jwt-refresh"),
]
