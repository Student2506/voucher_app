"""Views to serve vista objects."""

import json
import os
from typing import Any

import pika
from django.http import JsonResponse
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.request import Request

from vista_module.models import Customer, VoucherType
from voucher_api.serializers import (
    CustomerDetailSerializer,
    CustomerListSerializer,
    RequestOrderSerializer,
    VoucherTypeOrderingSerializer,
)

RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', None)


class CustomerViewset(viewsets.ReadOnlyModelViewSet):
    """API Endpoint which allows to view Customers."""

    queryset = Customer.objects.using('vista')

    def get_serializer_class(self) -> serializers.ModelSerializer:
        """Choose serializer.

        Returns:
            serializers.ModelSerializer - instance to use
        """
        if self.action == 'retrieve':
            return CustomerDetailSerializer
        return CustomerListSerializer


class VoucherTypeViewset(viewsets.ModelViewSet):
    """API Endpoint which chooses VoucherType."""

    queryset = VoucherType.objects.using('vista')
    serializer_class = VoucherTypeOrderingSerializer


@api_view(['POST'])
def put_order(request: Request, order_item_id: int) -> JsonResponse:
    """Make request to send vouchers.

    Args:
        request: Request - data to create order
        order_item_id: int - item to create order

    Returns:
        JsonResponse - status of creation or failure
    """
    order_data = JSONParser().parse(request)
    order_data['order_item'] = int(order_item_id)
    order = RequestOrderSerializer(data=order_data)
    if order.is_valid():
        order.save()
        send_data_to_generation(order_data)
        return JsonResponse(order.data, status=status.HTTP_201_CREATED)
    return JsonResponse(order.errors, status=status.HTTP_400_BAD_REQUEST)


def send_data_to_generation(body: dict[str, Any]) -> None:
    """Send data to worker.

    Args:
        body: dict - data to create voucher upon
    """
    connection = pika.BlockingConnection(
        pika.URLParameters(os.getenv('RABBITMQ_URL')),
    )
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    channel.basic_publish(
        exchange='',
        routing_key=RABBITMQ_QUEUE,
        body=json.dumps(body),
    )
    connection.close()
