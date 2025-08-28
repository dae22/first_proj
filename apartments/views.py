from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from apartments.models import Apartments


@api_view(["POST"])
def add_apartment(request):
    description = request.data.get("description")
    price = request.data.get("price")
    if not description:
        return JsonResponse({"error": "Description is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not price or price <= 0 or not isinstance(price, float):
        return JsonResponse(
            {"error": "Price is required and must be positive"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    new_apt = Apartments(description=description, price=price)
    new_apt.save()
    return JsonResponse(
        {"message": "New apartment added successfully", "apartment_id": new_apt.pk},
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
def get_apartments(request):
    apts = Apartments.objects.all()
    data = [{"id": apt.id, "description": apt.description, "price": apt.price} for apt in apts]
    return HttpResponse(data)


@api_view(["PATCH"])
def change_apartment(request, apt_id):
    changed_apt = Apartments.objects.get(pk=apt_id)
    description = request.data.get("description")
    price = request.data.get("price")
    if description:
        changed_apt.description = description
    if price:
        changed_apt.price = price
    changed_apt.save()
    return HttpResponse(f"Apartment {apt_id} has been changed")


@api_view(["DELETE"])
def delete_apartment(request, apt_id):
    Apartments.objects.filter(pk=apt_id).delete()
    return HttpResponse(f"Apartment {apt_id} has been deleted")
