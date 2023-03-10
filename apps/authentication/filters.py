from django_filters import rest_framework as filters
from .models import User


class UserFilter(filters.FilterSet):
    filter = filters.CharFilter(
        method="filter_username_email_full_name",
        help_text="Filter contains user.nama, email, or full name",
    )
