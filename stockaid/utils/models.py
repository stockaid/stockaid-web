from django.db import models
from django.contrib.auth import get_user_model

from model_utils import choices
from model_utils.fields import MonitorField
from model_utils.models import SoftDeletableModel, StatusModel, TimeStampedModel

User = get_user_model()


class UserStampedModel(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class BaseModel(TimeStampedModel, models.Model):
    class Meta:
        abstract = True
