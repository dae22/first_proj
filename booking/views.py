from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView

from booking.models import Booking
from booking.serializers import BookingSerializer


class BookingAPIView(APIView):
    def get(self, request, id):
        if bookings := Booking.objects.filter(apartment_id=id):
            data = BookingSerializer(bookings, many=True).data
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
        return JsonResponse({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save()
            return JsonResponse({"message": f"Booking id: {booking.pk}"}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        booking = get_object_or_404(Booking, pk=id)
        booking.delete()
        return JsonResponse({"message": "Booking deleted"}, status=status.HTTP_204_NO_CONTENT)
