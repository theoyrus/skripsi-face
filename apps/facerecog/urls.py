from django.urls import path, re_path, include
from rest_framework import routers
from .views import (
    index,
    CitraWajahViewset,
    CitraWajahList,
    CitraWajahTraining,
    CitraWajahRecognize,
)

# from facerecog
citrawajah_viewset = CitraWajahViewset.as_view({"get": "list", "post": "create"})
citrawajah_list = CitraWajahList.as_view()

from core.helpers import OptionalSlashRouter

router = OptionalSlashRouter()
router.register("citrawajah", CitraWajahViewset, basename="citrawajah")

urlpatterns = [
    # re_path(r"", index, name="index"),
    re_path(r"", include(router.urls)),
    # re_path(r"/citrawajah", include(router.urls)),
    # path("/citrawajah", citrawajah_list),
    # re_path(r"/citrawajah", citrawajah_viewset, name="citrawajah-list"),
    # re_path(r"/citrawajah", citrawajah_list, name="citrawajah-list"),
    path("training", CitraWajahTraining.as_view(), name="training"),
    path("recognize", CitraWajahRecognize.as_view(), name="recognize"),
]
