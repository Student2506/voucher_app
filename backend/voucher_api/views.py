"""Views to serve vista objects."""

import json
import logging
import os
import time
from datetime import datetime
from typing import Any

import jwt
import pika
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import (
    decorators,
    filters,
    mixins,
    serializers,
    status,
    views,
    viewsets,
)
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from vista_module.models import Customer, OrderItem, Stock, VoucherType
from voucher import settings
from voucher_api.serializers import (
    CustomerDetailSerializer,
    CustomerListSerializer,
    OrderItemItemSerializer,
    OrderItemListSerializer,
    RequestOrderSerializer,
    StockSerializer,
    StockWriteSerializer,
    VoucherTypeOrderingSerializer,
)
from voucher_app.logging import request_id, username

RABBITMQ_QUEUE_INCOMING = os.getenv('RABBITMQ_QUEUE_INCOMING', None)
logger = logging.getLogger(__name__)


class CustomerViewset(viewsets.ReadOnlyModelViewSet):
    """API Endpoint which allows to view Customers."""

    queryset = Customer.objects.using('vista').order_by('customer_name')
    filter_backends = [filters.SearchFilter]
    search_fields = ['customer_name']

    def get_serializer_class(self) -> serializers.ModelSerializer:
        """Choose serializer.

        Returns:
            serializers.ModelSerializer - instance to use
        """
        logger.info('Accessing customers view')
        if self.action == 'retrieve':
            return CustomerDetailSerializer
        return CustomerListSerializer

    def retrieve(self, request: Request, *args: list[Any], **kwargs: dict[Any, Any]) -> Response:
        result = super().retrieve(request, *args, **kwargs)
        logger.info(result.data)
        return result


class VoucherTypeViewset(viewsets.ModelViewSet):
    """API Endpoint which chooses VoucherType."""

    queryset = VoucherType.objects.using('vista')
    serializer_class = VoucherTypeOrderingSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['voucher_description']

    def get_queryset(self) -> Any:
        logger.info('Accessing voucher view')
        return super().get_queryset()


class OrderItemViewset(viewsets.ModelViewSet):
    """API Endpoint to query order_items"""

    queryset = OrderItem.objects.using('vista')
    filter_backends = [filters.SearchFilter]

    def get_serializer_class(self) -> serializers.ModelSerializer:
        logger.info('Accessing OrderItem view')
        if self.action == 'retrieve':
            return OrderItemItemSerializer
        return OrderItemListSerializer

    def retrieve(self, request: Request, *args: list[Any], **kwargs: dict[Any, Any]) -> Any:
        result = super().retrieve(request, *args, **kwargs)
        logger.info(result.data)
        return result


class StockViewset(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """API Endpoint to query order_items"""

    queryset = Stock.objects.using(
        'vista'
    ).filter(
        voucher_type_id__vouchertype_strgiftcard='Y'
    ).exclude(
        issued_date='1900-01-01 00:00:00.000'
    )
    serializer_class = StockSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['stock_strbarcode', 'client_order_item__order_id__order_id']

    def get_queryset(self) -> Any:
        logger.info('Access to order_items View')
        return super().get_queryset()


@csrf_exempt
@decorators.api_view(['POST'])
def put_order(request: Request, order_item_id: int) -> Response:
    """Make request to send vouchers.

    Args:
        request: Request - data to create order
        order_item_id: int - item to create order

    Returns:
        Response - status of creation or failure
    """
    logger.info('Access Put order view')
    order_data = JSONParser().parse(request)
    order_data['addresses'] = order_data.get('addresses').split(';')
    order_data['order_item'] = int(order_item_id)
    order_data['request_id'] = request_id.get()
    order_data['username'] = username.get()
    logger.info(order_data)
    if request.query_params.get('codetype', None) == 'qrcode':
        order_data['codetype'] = 'qrcode'
    order = RequestOrderSerializer(data=order_data)
    if order.is_valid():
        order.save()
        send_data_to_generation(order_data)
        return Response(order.data, status=status.HTTP_201_CREATED)
    return Response(order.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateExpiry(views.APIView):

    def get_object(self, obj_id: str) -> Any:
        logger.info('Access to Update Expiry View')
        try:
            return Stock.objects.using('vista').get(stock_strbarcode=obj_id)
        except (Stock.DoesNotExist, ValidationError):
            raise

    def validate_ids(self, obj_list: list[str]) -> bool:
        for code in obj_list:
            try:
                Stock.objects.using('vista').get(stock_strbarcode=code)
            except (Stock.DoesNotExist, ValidationError):
                raise
        return True

    def put(self, request: Request, *args: list[Any], **kwargs: dict[Any, Any]) -> Response:
        logger.info('Request to Update Expiry with update')
        codes = request.data['codes']
        logger.info(codes)
        try:
            self.validate_ids(codes)
        except (Stock.DoesNotExist, ValidationError):
            return Response(status=status.HTTP_404_NOT_FOUND)
        new_expiry_objs = Stock.objects.using('vista').filter(stock_strbarcode__in=codes)
        new_expiry_objs.update(expiry_date=request.data['extend_date'])
        serializer = StockWriteSerializer(new_expiry_objs, many=True)
        return Response(serializer.data)


def send_data_to_generation(body: dict[str, Any]) -> None:
    """Send data to worker.

    Args:
        body: dict - data to create voucher upon
    """
    connection = pika.BlockingConnection(
        pika.URLParameters(os.getenv('RABBITMQ_URL')),
    )
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE_INCOMING)
    message = json.dumps(body)
    logger.info(f'Data is being sent to processing: {message}')
    channel.basic_publish(
        exchange='',
        routing_key=RABBITMQ_QUEUE_INCOMING,
        body=message,
    )
    connection.close()


@decorators.api_view(['GET'])
def retrieve_token(request: Request) -> Response:
    """Make request to send vouchers.

    Args:
        request: Request - data to create order

    Returns:
        Response - status of creation or failure
    """
    refresh = RefreshToken.for_user(request.user)
    userinfo = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    access = jwt.decode(
        userinfo['access'],
        str(settings.SIMPLE_JWT.get('SIGNING_KEY')),
        algorithms=[str(settings.SIMPLE_JWT.get('ALGORITHM'))],
    )
    refresh = jwt.decode(
        userinfo['refresh'],
        str(settings.SIMPLE_JWT.get('SIGNING_KEY')),
        algorithms=[str(settings.SIMPLE_JWT.get('ALGORITHM'))],
    )
    response = redirect('/vouchers')
    response.set_cookie(
        'auth_access',
        value=userinfo['access'].strip("'"),
        secure=False,
        expires=datetime.fromtimestamp(access['exp']),
    )
    response.set_cookie(
        'auth_refresh',
        value=userinfo['refresh'].strip("'"),
        secure=False,
        expires=datetime.fromtimestamp(refresh['exp']),
    )
    response['Authorization'] = f"JWT {userinfo['access']}"
    return response


@decorators.api_view(['GET'])
def clear_session(request: Request) -> Response:
    """Make request to send vouchers.

    Args:
        request: Request - data to create order

    Returns:
        Response - status of creation or failure
    """
    response = redirect('/sign-in')
    response.set_cookie(
        'auth_access',
        value='',
        secure=False,
        expires=datetime.fromtimestamp(time.time()),
    )
    response.set_cookie(
        'auth_refresh',
        value='',
        secure=False,
        expires=datetime.fromtimestamp(time.time()),
    )
    return response
