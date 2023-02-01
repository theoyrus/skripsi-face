from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from apps.facerecog.models import CitraWajah
from core.settings import MEDIA_ROOT


@receiver(pre_save, sender=CitraWajah)
def image_pre_save(sender, instance, *args, **kwargs):
    from core.helpers import logger

    if instance is None:
        pass
    else:
        try:
            # hapus gambar lama ketika update data citra
            # logger.warning("Signal executed")
            previous = CitraWajah.objects.get(citrawajah_id=instance.citrawajah_id)

            old_citra = f"{MEDIA_ROOT}/{previous.nama}"
            import os

            if os.path.exists(old_citra):
                os.remove(old_citra)
        except:
            pass


def image_post_delete(sender, instance, *args, **kwargs):
    try:
        instance.nama.delete(save=False)
    except:
        pass


post_delete.connect(image_post_delete, sender=CitraWajah)
# pre_save.connect(image_pre_save, sender=CitraWajah)
