# from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions, filters
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import NotFound

from .serializers import (
    CitraWajah,
    CitraWajahKaryawanSerializer,
    CitraWajahRecognizeSerializer,
    CitraWajahUploadSerializer,
)
from .permissions import CitrawajahModelPermissions
from .filters import CitraWajahFilter
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
def index(request):
    return JsonResponse({"message": "Face Recog :)"})


class CitraWajahViewset(ModelViewSet):
    """
    API endpoint mengelola citra wajah
    """

    parser_class = (FileUploadParser,)
    serializer_class = CitraWajahKaryawanSerializer
    permission_classes = [permissions.IsAuthenticated, CitrawajahModelPermissions]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CitraWajahFilter
    search_fields = ["karyawan__nama", "nama"]

    def get_serializer_class(self):
        if self.action in ["create"]:
            return CitraWajahUploadSerializer
        return self.serializer_class

    def get_queryset(self):
        try:
            user = self.request.user
            from core.helpers import logger

            # logger.warning(f"punya permission {user.get_all_permissions()}")
            logger.warning(
                f"punya permission { user.has_perm('facerecog.view_another_citrawajah') }"
            )
            if user.has_perm("facerecog.view_another_citrawajah"):
                # jika punya hak view semua citra wajah
                if "karyawan_id" in self.kwargs:
                    # tapi jika ada path param berisi karyawan_id, filter citra wajah milik karyawan tersebut
                    karyawan_id = self.kwargs["karyawan_id"]
                else:
                    # jika tidak ada path param, ambil seluruh objek citra
                    return CitraWajah.objects.all()
            else:
                # jika tidak punya hak view semua citra wajah, filter by sesi karyawan
                karyawan_id = user.user_karyawan.karyawan_id

            return CitraWajah.objects.filter(karyawan_id=karyawan_id)
        except ObjectDoesNotExist:
            from core.helpers.exception_api import KaryawanUserError

            raise KaryawanUserError("Sesi karyawan belum diatur")


class CitraWajahList(APIView):
    """
    Endpoint data citra wajah
    """

    def get(self, request, format=None):
        data = CitraWajah.objects.all()
        serializer = CitraWajahKaryawanSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CitraWajahKaryawanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CitraWajahKaryawanList(generics.ListAPIView):
    serializer_class = CitraWajahKaryawanSerializer

    def get_queryset(self):
        karyawan_id = self.kwargs["karyawan_id"]

        return CitraWajah.objects.filter(karyawan_id=karyawan_id)


class CitraWajahTraining(APIView):
    """
    Endpoint training citra wajah
    """

    def post(self, request, format=None):
        from facerecog.jobs import training_job

        train = training_job()
        return Response({"training": train, "request": request.POST})


class CitraWajahRecognize(APIView):
    """
    Endpoint recognize citra wajah
    """

    parser_class = (FileUploadParser,)
    serializer_class = CitraWajahRecognizeSerializer

    def get(self, request):
        return Response(
            {"message": "POST file field bernama citra untuk recognize wajah"}
        )

    def post(self, request, format=None):
        serializer = CitraWajahRecognizeSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        citra = request.FILES["citra"]
        from .recognizer import FacialRecognizer

        recognizer = FacialRecognizer()
        id, confidence = recognizer.recognize_citra(citra)
        percent_num, percent = recognizer.confidence2percent(confidence=confidence)
        # percent_num = round(100 - confidence)
        # percent = "{0}%".format(round(100 - confidence))
        if percent_num <= 50:
            id = 0
        from core.helpers import logger

        logger.warning(
            f"predicted id: {id} confidence: {confidence} percent: {percent}"
        )
        from apps.karyawan.models import Karyawan
        from apps.karyawan.serializers import KaryawanRecognizeSerializer

        karyawan = Karyawan.objects.filter(karyawan_id=id)
        serializer_context = {
            "request": request,
        }
        serializer = KaryawanRecognizeSerializer(
            karyawan, many=True, context=serializer_context
        )
        httpstatus = status.HTTP_200_OK
        if id == 0:
            raise NotFound(detail="Wajah tidak dikenali")

        return Response(
            {
                "data": {
                    "confidence": confidence,
                    "percent": percent,
                    "karyawan": serializer.data[0]
                    if serializer.data.__len__() > 0
                    else None,
                    # "karyawan": karyawan,
                }
            },
            status=httpstatus,
        )
