from uuid import uuid4
from django.db import models
import random


class SupportedDatabase(models.Model):
    database_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.database_name


class ApiToken(models.Model):
    token = models.CharField(max_length=255, unique=True, blank=True)
    purpose = models.CharField(max_length=255, help_text="token purpose")
    owner = models.CharField(max_length=255)
    allowed_databases = models.ManyToManyField(SupportedDatabase)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            token = ""

            for t in str(uuid4()):
                if random.randint(0, 1) == 0:
                    t = t.upper()
                else:
                    t = t.lower()
                token += t
            self.token = token

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.purpose

