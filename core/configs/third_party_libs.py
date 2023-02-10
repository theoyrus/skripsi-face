from datetime import timedelta
from ..settings import env, random_secret, STATIC_URL
from django.urls import reverse_lazy


# Simple JWT Implementation
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": env.str("SECRET_KEY", default=random_secret),
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": (
        "Bearer",
        "JWT",
        "Token",
    ),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

import datetime

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token["iat"] = datetime.datetime.now()
#         token["user"] = user.username
#         token["date"] = str(datetime.date.today())

#         return token


# DJOSER auth boilerplate
# https://djoser.readthedocs.io/en/latest/settings.html
DJOSER = {
    "SEND_ACTIVATION_EMAIL": env.bool("DJOSER_SEND_ACTIVATION_EMAIL", default=False),
    "PASSWORD_RESET_CONFIRM_URL": "main/users/reset_password/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "#/username/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "accounts/activate/{uid}/{token}",
    "SERIALIZERS": {
        # "user_create": "main.serializers.UserCreateSerializer",
    },
    # "LOGIN_FIELD": "email",
}

# Django Debug Toolbar Allowed IPS
INTERNAL_IPS = [
    "127.0.0.1",
]

# DRF Spectacular Settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Face Recognition Attendance APIs",
    "DESCRIPTION": "Daftar Endpoint API Sistem",
    "VERSION": "1.0.0",
    # "PREPROCESSING_HOOKS": ["spectacular.hooks.remove_apis_from_list"],
    # Custom Spectacular Settings
    "EXCLUDE_PATH": [reverse_lazy("schema")],
}

JAZZMIN_SETTINGS = {
    "site_title": "Face Recognition",
    "site_header": "Presensi Wajah",
    "site_brand": "Presensi Wajah",
    "site_logo": "icon.png",
    "welcome_sign": "Presensi Wajah",
    "copyright": "Suryo Prasetyo Wibowo",
    "show_ui_builder": False,
    # side menu
    "order_with_respect_to": ["auth", "main", "karyawan", "facerecog"],
    # custom
    "custom_css": "css/jazzmin.css",
}

JAZZMIN_UI_TWEAKS = {
    "sidebar_nav_compact_style": True,
    "sidebar_nav_flat_style": True,
    "navbar_fixed": True,
    "sidebar_fixed": True,
    "related_modal_active": True,
}

DRF_STANDARDIZED_ERRORS = {
    "EXCEPTION_FORMATTER_CLASS": "core.helpers.exception_api.ApiExceptionFormatter"
}
