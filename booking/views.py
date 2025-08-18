from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

from apartments.models import Apartments
from booking.models import Booking


@api_view(["POST"])
def add_booking(request):
    start = request.data.get("start")
    end = request.data.get("end")
    apartment = Apartments.objects.get(pk=request.data.get("apt_id"))
    new_booking = Booking(apartment=apartment, start=start, end=end)
    new_booking.save()
    return JsonResponse({"booking_id": new_booking.pk})


@api_view(["GET"])
def get_booking(request, apt_id):
    bookings = Booking.objects.all()
    data = [
        {
            "booking_id": b.pk,
            "start_date": b.start.isoformat(),
            "end_date": b.end.isoformat(),
        }
        for b in bookings
    ]
    data.sort(key=lambda x: x["start_date"])
    return HttpResponse(data)


@api_view(["DELETE"])
def delete_booking(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    booking.delete()
    return JsonResponse({"Delete booking": "success"})
