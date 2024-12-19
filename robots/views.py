import json

import logging.config

from django.core.exceptions import ValidationError
from django.http import FileResponse, JsonResponse
from django.views import View

from robots.handlers import create_df_week, generate_serial, write_to_excel

from .models import Robot
from config_log.logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
error_logger = logging.getLogger('log_error')
debug_logger = logging.getLogger('log_debug')
info_logger = logging.getLogger('log_info')

class RobotCreate(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            model = data.get("model")
            version = data.get("version")
            robot = Robot(model=model, version=version, created=data['created'])
            robot.serial = generate_serial(model, version)
            robot.save()
            info_logger.info("Robot created successfully: %s", robot.serial)
            return JsonResponse({"message": "Robot created successfully!"}, status=201)
        except KeyError as e:
            error_logger.error("Missing key: %s", e)
            return JsonResponse({"error": f"Missing key: {str(e)}"}, status=400)
        except ValidationError as e:
            error_logger.error("Validation error: %s", e.messages)
            return JsonResponse({"error": e.messages}, status=400)
        except Exception as e:
            error_logger.error("Unexpected error:", exc_info=True)
            return JsonResponse({"error": str(e)}, status=500)


class RobotWeek(View):
    def get(self, request,  *args, **kwargs):
        grouped = create_df_week()
        try:
            file_path = write_to_excel(grouped)
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='robots_report.xlsx')
        except Exception as e:
            error_logger.error("Error write file:", str(e))
            return JsonResponse({"error": e}, status=400)