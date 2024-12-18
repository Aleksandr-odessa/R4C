from django.urls import path

from .views import RobotCreate

urlpatterns = [
    path('robots/create/', RobotCreate.as_view(), name='robot-create'),
]
