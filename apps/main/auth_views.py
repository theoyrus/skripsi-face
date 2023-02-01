from django.contrib.auth.views import PasswordResetView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

import requests


class UserActivationView(APIView):
    # Handle Link Aktivasi by URL dari email
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "accounts/activation.html"

    def get(self, request, uid, token):
        protocol = "https://" if request.is_secure() else "http://"
        web_url = protocol + request.get_host()
        post_url = web_url + "/auth/users/activation/"
        post_data = {"uid": uid, "token": token}
        result = requests.post(post_url, data=post_data)
        if result.status_code == 204:
            content = {"success": True, "detail": "Successfuly Activated :)"}
        else:
            content = result.json
        return Response({"data": content})


class UserPasswordResetView(PasswordResetView):
    # Handle Link Res by URL dari email
    template_name = "accounts/password_reset.html"
