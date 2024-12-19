import pandas as pd
from datetime import timedelta
from django.utils import timezone

from robots.models import Robot


def generate_serial(model, version):
    return f'{model}-{version}'

def create_df_week():
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    last_week_start = start_of_week - timedelta(weeks=1)
    robots = Robot.objects.filter(created__gte=last_week_start)
    data = [{'model': robot.model, 'version': robot.version} for robot in robots]
    return frame_with_count(data)


def frame_with_count(data_in):
    df = pd.DataFrame(data_in)
    grouped = df.groupby(["model", "version"]).size().reset_index(name='count')
    grouped.rename(columns={
        'model': 'Модель',
        'version': 'Версия',
        'count': 'Количество за неделю'
    })
    return grouped

def write_to_excel(grouped_model):
    file_path = 'output.xlsx'
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        for model in grouped_model['Модель']:
            model_data = grouped_model[grouped_model['Модель'] == model]
            model_data.to_excel(writer, sheet_name=model, index=False)
    return file_path
