import re

from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Customer



@receiver(pre_save, sender=Customer)
def verifications(sender, instance, **kwargs):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, instance.email):
        raise ValidationError("E-mail is not correct")

