from django.apps import AppConfig


class KaryawanConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.karyawan"
    verbose_name: str = "Modul Karyawan"

    def ready(self) -> None:
        import apps.karyawan.signals
