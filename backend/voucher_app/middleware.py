import logging
from http import HTTPStatus
from typing import Callable

import jwt
from django.http import HttpRequest, HttpResponse

from voucher import settings
from voucher_app.logging import request_id, username

logger = logging.getLogger(__name__)


class RequestIdMiddleware:

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.headers.get('X-Request-Id'):
            request_id.set(request.headers.get('X-Request-Id'))
        if request.headers.get('Authorization'):
            token = request.headers.get('Authorization').lstrip('JWT ')
            try:
                access = jwt.decode(
                    token,
                    str(settings.SIMPLE_JWT.get('SIGNING_KEY')),
                    algorithms=[str(settings.SIMPLE_JWT.get('ALGORITHM'))],
                )
            except jwt.exceptions.ExpiredSignatureError:
                return HttpResponse('Unauthorized', status=HTTPStatus.UNAUTHORIZED)
            username.set(access.get('user_id'))
        response = self.get_response(request)
        return response
