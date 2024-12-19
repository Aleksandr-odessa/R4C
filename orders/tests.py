import json

from django.test import Client, TestCase
from django.urls import reverse

from customers.models import Customer
from orders.models import Order


class RobotsOrderTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('robot-order')

    def test_create_order_success(self):
        """Test success creating order."""
        data = {
            "email": "test@example.com",
            "serial": "RX-D2"
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "Robot order successfully!"})

        self.assertTrue(Customer.objects.filter(email=data["email"]).exists())
        self.assertTrue(Order.objects.filter(robot_serial=data["serial"]).exists())

    def test_create_order_validation_error(self):
        """ Test_create_order_validation_error """

        data = {
            "serial": "RX-D2"
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': "Missing key: 'email'"} )
