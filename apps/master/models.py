from django.db import models
from django.contrib.auth import get_user_model

from apps.main.models import BaseModel


# Create your models here.
class UserPreferensi(BaseModel):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="user_pref"
    )
    pref = models.JSONField()

    class Meta:
        db_table = "preferensi"
        verbose_name_plural = "preferensi"

    def __str__(self):
        return self.user.username
