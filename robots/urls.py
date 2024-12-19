from django.urls import path

from .views import RobotCreate, RobotWeek

urlpatterns = [
    path('robots/create/', RobotCreate.as_view(), name='robot-create'),
    path('robots/week/', RobotWeek.as_view(), name = 'robot-week'),
]
