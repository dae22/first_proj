from django.db import models

from apartments.models import Apartments


class Booking(models.Model):
    apartment = models.ForeignKey(Apartments, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return f"Booking #{self.pk} for {self.apartment}"
