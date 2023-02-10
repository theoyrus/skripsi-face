"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import handler404, handler500
from core.helpers.exception_api import error404, error500

handler404 = error404
handler500 = error500
# handler500 = "rest_framework.exceptions.server_error"

# Third Party Libs
# from rest_framework import routers

from core.helpers import OptionalSlashRouter

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# import URLs from our apps to generated in OpenAPI
from apps.karyawan import views, urls

# router = routers.DefaultRouter(trailing_slash=False)
router = OptionalSlashRouter()
router.register("karyawan", views.KaryawanViewSet)
router.register("divisi", views.DivisiViewSet)

urlpatterns = [
    # path("", include("main.urls")),
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    # ================
    # Third Party Libs
    # rest_framework auth
    path("browsable-api-auth/", include("rest_framework.urls")),
    # djoser
    path("auth/", include("djoser.urls")),
    # if auth backend use JWT
    path("auth/", include("djoser.urls.jwt")),
    # if auth backend use Token Based
    path("auth/", include("djoser.urls.authtoken")),
    # DRF Spectacular
    re_path(r"api/schema", SpectacularAPIView.as_view(), name="schema"),
    re_path(
        r"api/docs\/?",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    re_path(
        r"api/redocs\/?",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc-ui",
    ),
    # ================
    # Local Apps
    re_path(r"auth/", include("apps.authentication.urls")),
    # re_path(r"main", include("apps.main.urls")),
    re_path(r"karyawan/", include("apps.karyawan.urls")),
    re_path(r"facerecog/", include("facerecog.urls")),
    # ================
    # Third Party Libs (optional)
    # djoser
    path("auth/", include("djoser.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    # Ini adalah urls patterns untuk menampikan django debug toolbar, hanya saat mode development
    urlpatterns += (
        path(
            "__debug__/",
            include(debug_toolbar.urls),
        ),
    )

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
