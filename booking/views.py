from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView

from apartments.models import Apartments
from booking.models import Booking


class BookingAPIView(APIView):
    def get(self, request):
        bookings = Booking.objects.filter(apartment_id=request.data.get("apartment_id"))
        if bookings.exists():
            data = [
                {
                    "booking_id": b.pk,
                    "start_date": b.start.isoformat(),
                    "end_date": b.end.isoformat(),
                }
                for b in bookings
            ]
            data.sort(key=lambda x: x["start_date"])
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        apartment = get_object_or_404(Apartments, pk=request.data.get("apt_id"))
        start = request.data.get("start")
        end = request.data.get("end")
        cross_booking = Booking.objects.filter(
            (Q(start__lte=start) & Q(end__gt=start))
            | (Q(start__lt=end) & Q(end__gte=end))
            | (Q(start__gte=start) & Q(end__lte=end)),
            apartment=apartment,
        )
        if not cross_booking.exists():
            new_booking = Booking.objects.create(apartment=apartment, start=start, end=end)
            return JsonResponse(
                {"message": f"New booking added with id: {new_booking.pk}"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return JsonResponse(
                {"error": "Booking dates cross with other booking"},
                status=status.HTTP_409_CONFLICT,
            )

    def delete(self, request):
        booking = get_object_or_404(Booking, pk=request.data.get("booking_id"))
        booking.delete()
        return JsonResponse({"message": "Booking deleted"}, status=status.HTTP_204_NO_CONTENT)
