from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.handlers import request_email
from robots.models import Robot


@receiver(post_save, sender=Robot)
def informant_on_email(sender, instance, created, **kwargs):
    if created:
        emails = request_email(instance.serial)
        model_version = instance.serial.split('-')
        send_mail(settings.EMAIL_HOST_USER,f'Добрый день! \n Недавно вы интересовались '
                                           f'нашим роботом модели {model_version[0]} версии {model_version[1]}\n'
              f'Этот робот теперь в наличии. '
              f'Если вам подходит этот вариант - пожалуйста, свяжитесь с нами',
                'mail@mail.ru',[emails],
                fail_silently=False)