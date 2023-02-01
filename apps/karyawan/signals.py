from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Karyawan


@receiver(post_save, sender=User, dispatch_uid="save_new_user_karyawan")
def save_karyawan(sender, instance, created, **kwargs):
    if created:
        Karyawan.objects.create(
            user=instance,
            nama=instance.first_name + " " + instance.last_name,
        )
        # karyawan = Karyawan(user=instance)
        # karyawan.save()
