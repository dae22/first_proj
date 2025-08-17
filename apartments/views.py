from django.http import HttpResponse
from rest_framework.decorators import api_view

from apartments.models import Apartments


@api_view(["POST"])
def add_apartment(request):
    description = request.POST.get("description")
    price = request.POST.get("price")
    new_apt = Apartments(description=description, price=price)
    new_apt.save()
    return HttpResponse(f"New apartment added with id: {new_apt.pk}")


@api_view(["GET"])
def get_apartments(request):
    apts = Apartments.objects.all()
    data = [
        {"id": apt.id, "description": apt.description, "price": apt.price}
        for apt in apts
    ]
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
