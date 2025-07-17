"""
The core application: middleware definitions for request/response cycle.
"""

from django.http import HttpResponse

HEALTHCHECK_PATH = "/healthcheck"


class Healthcheck:
    """Middleware intercepts and accepts /healthcheck requests."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == HEALTHCHECK_PATH:
            return HttpResponse("Healthy", content_type="text/plain")
        return self.get_response(request)
