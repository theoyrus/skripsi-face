from ..settings import env, DJANGO_APPS

# Per Project Custom Settings

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_standardized_errors",
    "drf_spectacular",
    "debug_toolbar",
    "corsheaders",
    "djoser",
    "django_filters",
]

LOCAL_APPS = [
    # Add our apps below
    "apps.main",
    "apps.authentication",
    "apps.karyawan",
    "apps.facerecog",
    "apps.presensi",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    # Middleware django debug toolbar yang kita gunakan di mode development
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # Add Custom Middleware before Django Middleware, below
    # Middleware whitenoise is easy handle static file in production
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # Middleware Django CORS
    "corsheaders.middleware.CorsMiddleware",
    # ==========================
    # Below is Django Middleware
    # ==========================
    # "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "core.middleware.CommonMiddlewareAppendSlashWithoutRedirect",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# User Model
AUTH_USER_MODEL = "authentication.User"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
REQUIRED_FIELDS = ["username", "email"]


# Only on Development! Backend Email use console, comment if not used
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Only on Development! Backend Email use file, comment if not used
# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = str(proj_dir + 'deploy/sent_emails/')

# Default Email Backend Django (smtp), use this or above
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
MAILER_EMAIL_BACKEND = EMAIL_BACKEND
EMAIL_HOST = env.str("EMAIL_DEF_SMTP", default="0.0.0.0")
EMAIL_HOST_USER = env.str("EMAIL_DEF_USER", default="")
EMAIL_HOST_PASSWORD = env.str("EMAIL_DEF_PASS", default="")
EMAIL_PORT = env.int("EMAIL_DEF_PORT", default=1025)
EMAIL_USE_TLS = False
# EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = env.str("EMAIL_DEF_FROM", default=EMAIL_HOST_USER)

TIME_ZONE = "Asia/Jakarta"

from ..settings import storage_root

ASSETS_ROOT = storage_root("assets")

X_FRAME_OPTIONS = "SAMEORIGIN"
