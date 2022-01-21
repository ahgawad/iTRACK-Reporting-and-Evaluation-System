from django.http import JsonResponse
from django.core.exceptions import RequestDataTooBig
import logging

class CheckRequest(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        return response

    def process_exception(self, request, exception):
        logger = logging.getLogger(__name__)
        logger.error('process_exception: HERE!!!')
        if isinstance(exception, RequestDataTooBig):
            logger.error('process_exception: HERE 2!!!')
            return JsonResponse({"error":"file is too big"})