import datetime
import json

from django.test import TestCase
from django.urls import reverse

from robots.models import Robot


class RobotCreateViewTest(TestCase):
    def setUp(self):
        self.url = reverse('robot-create')

    def test_create_robot_success(self):
        """Test success creating robots."""
        data = {
            "model": "RX",
            "version": "D2",
            "created": "2022-12-31 23:59:59"
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "Robot created successfully!"})
        self.assertEqual(Robot.objects.count(), 1)
        robot = Robot.objects.first()
        self.assertEqual(robot.model, "RX")
        self.assertEqual(robot.version, "D2")
        self.assertEqual(robot.serial, "RX-D2")
        self.assertEqual(robot.created, datetime.datetime(2022, 12, 31, 23, 59, 59))

    def test_create_robot_invalid_model(self):
        """Test invalid length of field "model" """
        data = {
            "model": "RX3",
            "version": "D2",
            "created": "2022-12-31 23:59:59"
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),   {'error': ['The length of the "model" field must be only 2 characters.']})

    def test_create_robot_invalid_version(self):
        """Test invalid length of field "version" """
        data = {
            "model": "RX",
            "version": "D22",
            "created": "2022-12-31 23:59:59"
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),   {'error': ['The length of the "version" field must be only 2 characters.']})

    def test_create_robot_invalid_date(self):
        """Test invalid field "created" """
        data = {
            "model": "RX",
            "version": "D2",
            "created": "23:59:59 2022-12-31 "
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),   {'error': ["Created must be in the format 'YYYY-MM-DD HH:MM:SS'"]})

    def test_create_robot_empty_model(self):
        """ Test-empty field 'model'"""
        data = {
            "model": "",
            "version": "D2",
            "created": "23:59:59 2022-12-31 "
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': ['Model, version, and created fields must be provided.']})

    def test_create_robot_invalid_json(self):
        """test  invalid format json"""
        data = {
            "model": "RX",
            "version": "D2",
            "creat": "2022-12-31 23:59:59"
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': "Missing key: 'created'"})
