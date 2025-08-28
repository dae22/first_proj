from django.db import models

from apartments.models import Apartments


class Booking(models.Model):
    apartment = models.ForeignKey(Apartments, on_delete=models.CASCADE, related_name="bookings")
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return f"Booking #{self.id} for {self.apartment}"
