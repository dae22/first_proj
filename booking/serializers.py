from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apartments.models import Apartments
from booking.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    apartment_id = serializers.IntegerField(write_only=True)
    booking_id = serializers.IntegerField(read_only=True, source="id")

    class Meta:
        model = Booking
        fields = ["booking_id", "apartment_id", "start_date", "end_date"]

    def validate(self, data):
        apartment_id = data["apartment_id"]
        start = data["start_date"]
        end = data["end_date"]

        cross_booking = Booking.objects.filter(
            (Q(start_date__lte=start) & Q(end_date__gt=start))
            | (Q(start_date__lt=end) & Q(end_date__gte=end))
            | (Q(start_date__gte=start) & Q(end_date__lte=end)),
            apartment_id=apartment_id,
        )
        if cross_booking.exists():
            raise serializers.ValidationError("Booking dates cross with other bookings")

        return data

    def create(self, validated_data):
        apartment_id = validated_data.pop("apartment_id")
        apartment = get_object_or_404(Apartments, pk=apartment_id)
        return Booking.objects.create(apartment=apartment, **validated_data)
