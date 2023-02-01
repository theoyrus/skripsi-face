from rest_framework.routers import DefaultRouter, SimpleRouter

# Make slash suffix in django optional, https://stackoverflow.com/a/46163870
class SimpleOptionalSlashRouter(SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = "/?"


class OptionalSlashRouter(DefaultRouter):
    def __init__(self, *args, **kwargs):
        super(DefaultRouter, self).__init__(*args, **kwargs)
        self.trailing_slash = "/?"
