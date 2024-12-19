import json

import logging.config

from django.core.exceptions import ValidationError
from django.http import FileResponse, JsonResponse
from django.views import View

from customers.models import Customer
from orders.models import Order
from config_log.logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
error_logger = logging.getLogger('log_error')
debug_logger = logging.getLogger('log_debug')
info_logger = logging.getLogger('log_info')

class RobotsOrder(View):
    def post(self, request,  *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        try:
            customer = Customer(email=data['email'])
            customer.save()
        except KeyError as e:
            error_logger.error("Missing key: %s", e)
            return JsonResponse({"error": f"Missing key: {str(e)}"}, status=400)
        except ValidationError as e:
            error_logger.error("Validation error:", e.messages)
            return JsonResponse({"error": e.messages}, status=400)
        except Exception:
            error_logger.error("Failed to save customer:", exc_info=True)
            return JsonResponse({"error": "Failed to save customer"}, status=500)

        try:
            order = Order(customer=customer, robot_serial=data["serial"])
            order.save()
        except Exception:
            error_logger.error("Failed to save order:", exc_info=True)
            return JsonResponse({"error": "Failed to save order"}, status=500)

        return JsonResponse({"message": "Robot order successfully!"}, status=201)

