from datetime import datetime

from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Robot


@receiver(pre_save, sender=Robot)
def verifications(sender, instance, **kwargs):
    if not all([instance.model, instance.version, instance.created]):
        raise ValidationError("Model, version, and created fields must be provided.")
    elif len(instance.model) != 2:
        raise ValidationError('The length of the "model" field must be only 2 characters.')
    elif len(instance.version) != 2:
        raise ValidationError('The length of the "version" field must be only 2 characters.')
    try:
        instance.created = datetime.strptime(instance.created, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ValidationError("Created must be in the format 'YYYY-MM-DD HH:MM:SS'")
