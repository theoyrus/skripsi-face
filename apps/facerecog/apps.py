from django.apps import AppConfig


class FacerecogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.facerecog"
    verbose_name: str = "Modul Face Recognition"

    def ready(self):
        # daftarkan signals yg ada di app ini
        import apps.facerecog.signals
