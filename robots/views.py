import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View

from .models import Robot


class RobotCreate(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            model = data.get("model")
            version = data.get("version")
            created = data.get("created")
            robot = Robot(model=model, version=version, created=created)
            robot.serial = RobotCreate.generate_serial(model, version)
            robot.save()
            return JsonResponse({"message": "Robot created successfully!"}, status=201)
        except ValidationError as e:
            return JsonResponse({"error": e.messages}, status=400)

    @staticmethod
    def generate_serial(model, version):
        return f'{model}-{version}'
