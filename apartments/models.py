from django.db import models


class Apartments(models.Model):
    description = models.CharField(max_length=255)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.description
