from django.utils import timezone
import pytz


def get_userpref_timezone(self):
    if hasattr(self, "request"):
        request = self.request
    elif hasattr(self, "context"):
        request = self.context.get("request")

    user = request.user
    if hasattr(user, "user_pref"):
        timezone_user = pytz.timezone(
            # user.user_pref.pref.get("timezone", timezone.get_default_timezone_name())
            user.user_pref.pref.get("timezone", "Asia/Jakarta")
        )
    else:
        # timezone_user = pytz.timezone(timezone.get_default_timezone_name())
        timezone_user = pytz.timezone("Asia/Jakarta")
    return timezone_user
