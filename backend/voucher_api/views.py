"""Views to serve vista objects."""

import json
import logging
import os
import time
from datetime import datetime
from typing import Any

import jwt
import pika
import pytz
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
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
from voucher_api import serializers as api_serializers
from voucher_app.logging import request_id, username
from voucher_app.models import Template

RABBITMQ_QUEUE_INCOMING = os.getenv('RABBITMQ_QUEUE_INCOMING', None)
logger = logging.getLogger(__name__)

VISTA_DATABASE = 'vista'


class CustomerViewset(viewsets.ReadOnlyModelViewSet):
    """API Endpoint which allows to view Customers."""

    queryset = Customer.objects.using(VISTA_DATABASE).order_by('customer_name')
    filter_backends = [filters.SearchFilter]
    search_fields = ['customer_name']

    def get_serializer_class(self) -> serializers.ModelSerializer:
        """Choose serializer.

        Returns:
            serializers.ModelSerializer - instance to use
        """
        logger.info('Accessing customers view')
        if self.action == 'retrieve':
            return api_serializers.CustomerDetailSerializer
        return api_serializers.CustomerListSerializer

    def retrieve(self, request: Request, *args: list[Any], **kwargs: dict[Any, Any]) -> Response:
        """Retreive data for logging.

        Args:
            request: Request - data to process
            args: list[Any] - arbitary list of positional arguments
            kwargs: list[Any, Any] - arbitary list of keyword arguments

        Returns:
            Response - proccessed data
        """
        response = super().retrieve(request, *args, **kwargs)
        logger.info(response.data)
        return response


class VoucherTypeViewset(viewsets.ModelViewSet):
    """API Endpoint which chooses VoucherType."""

    queryset = VoucherType.objects.using(VISTA_DATABASE)
    serializer_class = api_serializers.VoucherTypeOrderingSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['voucher_description']

    def get_queryset(self) -> Any:
        """Get data from database.

        Returns:
            Any - result of queryset
        """
        logger.info('Accessing voucher view')
        return super().get_queryset()


class OrderItemViewset(viewsets.ModelViewSet):
    """API Endpoint to query order_items."""

    queryset = OrderItem.objects.using(VISTA_DATABASE)
    filter_backends = [filters.SearchFilter]

    def get_serializer_class(self) -> serializers.ModelSerializer:
        """Get instance of serializer.

        Returns:
            ModelSerializer - instance of serializer
        """
        logger.info('Accessing OrderItem view')
        if self.action == 'retrieve':
            return api_serializers.OrderItemItemSerializer
        return api_serializers.OrderItemListSerializer

    def retrieve(self, request: Request, *args: list[Any], **kwargs: dict[Any, Any]) -> Any:
        """Get data for logging.

        Args:
            request: Request - data to process
            args: list[Any] - arbitary args
            kwargs: dict[Any, Any] - arbitary kwargs

        Returns:
            Any - processed data
        """
        order_data = super().retrieve(request, *args, **kwargs)
        logger.info(order_data.data)
        return order_data


class StockViewset(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
):
    """API Endpoint to query order_items."""

    queryset = Stock.objects.using(
        VISTA_DATABASE,
    ).filter(
        voucher_type_id__vouchertype_strgiftcard='Y',
    ).exclude(
        issued_date='1900-01-01 00:00:00.000',
    )
    serializer_class = api_serializers.StockSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['stock_strbarcode', 'client_order_item__order_id__order_id']
    filterset_fields = ['stock_strbarcode', 'client_order_item__order_id__order_id']

    def get_queryset(self) -> Any:
        """Get data from database.

        Returns:
            Any - result of queryset
        """
        logger.info('Access to order_items View')
        return super().get_queryset()

    def retrieve(self, request: Request, *args: list[Any], **kwargs: dict[Any, Any]) -> Any:
        """Get data for logging.

        Args:
            request: Request - data to process
            args: list[Any] - arbitary args
            kwargs: dict[Any, Any] - arbitary kwargs

        Returns:
            Any - processed data
        """
        stocks = super().retrieve(request, *args, **kwargs)
        logger.info(stocks.data)
        return stocks


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
    order_data['delivery'] = request.query_params.get('delivery', 'email')
    order_data['codetype'] = request.query_params.get('codetype', None)
    logger.info(order_data)
    order = api_serializers.RequestOrderSerializer(data=order_data)
    if order.is_valid():
        order.save()
        send_data_to_generation(order_data)
        return Response(order.data, status=status.HTTP_201_CREATED)
    return Response(order.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateExpiry(views.APIView):
    """View to consume update certs query."""

    def get_object(self, obj_id: str) -> Any:
        """Retreive object for view.

        Args:
            obj_id: str - id of object

        Returns:
            Any - object

        Raises:
            ValidationError: data provided is not valid
        """
        logger.info('Access to Update Expiry View')
        try:
            return Stock.objects.using(VISTA_DATABASE).get(stock_strbarcode=obj_id)
        except (Stock.DoesNotExist, ValidationError) as exc:
            logger.error(str(exc))
            raise

    def validate_ids(self, obj_list: list[str]) -> bool:
        """Check for provided ids are valid.

        Args:
            obj_list: list[str] - list of ids

        Returns:
            bool - result of validation

        Raises:
            ValidationError: wrong data provided
        """
        for code in obj_list:
            try:
                Stock.objects.using(VISTA_DATABASE).get(stock_strbarcode=code)
            except (Stock.DoesNotExist, ValidationError) as exc:
                logger.error(str(exc))
                raise
        return True

    def put(self, request: Request, *args: list[Any], **kwargs: dict[Any, Any]) -> Response:
        """Update vouchers with new expiry data.

        Args:
            request: Request - data to process
            args: list[Any] - arbitary list of args
            kwargs: dict[Any, Any] - arbitary list of kwargs

        Returns:
            Response - result of processing request
        """
        logger.info('Request to Update Expiry with update')
        codes = request.data['codes']
        logger.info(codes)
        logger.info(request.data.get('extend_date'))
        try:
            self.validate_ids(codes)
        except (Stock.DoesNotExist, ValidationError):
            return Response(status=status.HTTP_404_NOT_FOUND)
        new_expiry_objs = Stock.objects.using(VISTA_DATABASE).filter(stock_strbarcode__in=codes)
        non_expired_cards = new_expiry_objs.filter(expiry_date__gte=datetime.now(pytz.timezone('Europe/Moscow')))
        new_date = datetime.strptime(
            request.data.get('extend_date'),
            '%Y-%m-%d',
        )

        non_expired_cards.update(expiry_date=new_date.replace(tzinfo=pytz.UTC))
        serializer = api_serializers.StockWriteSerializer(non_expired_cards, many=True)
        return Response(serializer.data)

    def perform_update(self, serializer: Request) -> None:
        """Update vouchers with new expiry data.

        Args:
            serializer: Request - data to process
        """
        logger.info(pytz.timezone('Europe/Moscow'))
        logger.info(serializer)
        instance = serializer.save()
        logger.info(instance)


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
    access_token = userinfo['access']
    access = jwt.decode(
        access_token,
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
        value=access_token.strip("'"),
        secure=False,
        expires=datetime.fromtimestamp(access['exp']),
    )
    response.set_cookie(
        'auth_refresh',
        value=userinfo['refresh'].strip("'"),
        secure=False,
        expires=datetime.fromtimestamp(refresh['exp']),
    )
    response['Authorization'] = f'JWT {access_token}'
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


class TemplateViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """API Endpoint to adjust Templates."""

    queryset = Template.objects.all()
    serializer_class = api_serializers.TemplateSerializer

    def perform_update(self, serializer: serializers.ModelSerializer) -> Any:
        """Update Template with according serilizer.

        Args:
            serializer: serializers.ModelSerializer - Serializer to use with methods

        Returns:
            Any - may be anything...
        """
        if not serializer.initial_data.get('template_property'):
            return super().perform_update(serializer=serializer)
        for template_property in serializer.initial_data.get('template_property'):
            template_property_db_object = serializer.instance.properties.get(
                property_name=template_property.get('name'),
            )
            template_property_db_object.property_value = template_property.get('content')
            template_property_db_object.save()
        return super().perform_update(serializer=serializer)
