from django.urls import path
from . import views, auth_views

urlpatterns = [
    path("", views.index, name="index"),
    # handle activation djoser
    path(
        "users/activate/<str:uid>/<str:token>", auth_views.UserActivationView.as_view()
    ),
    # handle password reset djoser
    path("users/reset_password/", auth_views.UserPasswordResetView.as_view()),
    # handle password reset confirm djoser
    path(
        "users/activate/<str:uid>/<str:token>", auth_views.UserActivationView.as_view()
    ),
]
