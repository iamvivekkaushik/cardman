from django.db import models
from django.utils.text import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=30)

    def __str__(self):
        return self.name
