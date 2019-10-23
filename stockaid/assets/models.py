from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from model_utils.choices import Choices
from model_utils.fields import MonitorField
from model_utils.models import (
    SoftDeletableModel,
    StatusModel,
    TimeStampedModel,
)

from stockaid.utils.models import UserStampedModel

User = get_user_model()


class Category(TimeStampedModel, UserStampedModel, models.Model):
    name = models.CharField(_("Name of category"), max_length=255)
    description = models.TextField(_("Description of category"), blank=True)
    image = models.ImageField()

    def __str__(self):
        return self.name


class Location(TimeStampedModel, UserStampedModel, models.Model):
    name = models.CharField(_("Name of location"), max_length=255)
    description = models.TextField(_("Description of location"), blank=True)


class Manufacturer(TimeStampedModel, UserStampedModel, models.Model):
    name = models.CharField(_("Name of manufacturer"), max_length=255)
    description = models.TextField(_("Description of manufacturer"), blank=True)

    def __str__(self):
        return self.name


class AssetModel(TimeStampedModel, UserStampedModel, SoftDeletableModel,
                 models.Model):
    name = models.CharField(_("Name of asset-model"))
    description = models.TextField(_("Description of asset-model"), blank=True)
    category = models.ForeignKey("Category", on_delete=models.PROTECT)
    manufacturer = models.ForeignKey("Manufacturer", on_delete=models.PROTECT)
    code = models.CharField(_("Code specific to asset-model"), blank=True,
                            max_length=255)

    def __str__(self):
        return self.name


class Asset(TimeStampedModel, UserStampedModel, SoftDeletableModel,
            StatusModel, models.Model):
    STATUS = Choices(
        ('checked_out', 'Checked Out'),
        ('reserved', 'Reserved'),
    )

    name = models.CharField(_("Name of asset"))
    description = models.TextField(_("Description of asset"), blank=True)
    code = models.CharField(_("Code specific to asset"), blank=True,
                            max_length=255)

    asset_model = models.ForeignKey("AssetModel", on_delete=models.PROTECT)
    parent = models.ForeignKey("self", on_delete=models.PROTECT)
    location = models.ForeignKey("Location", on_delete=models.PROTECT)

    def __str__(self):
        return self.name
