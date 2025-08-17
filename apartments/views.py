from django.http import Http404, HttpResponse
from rest_framework import generics
from rest_framework.decorators import api_view

from apartments.models import Apartments
from apartments.serializers import ApartmentsSerializer


def delete_apartment(request, apt_id):
    if not apt_id:
        raise Http404()
    pass


@api_view(["POST"])
def add_apartment(request):
    new_apt = ApartmentsSerializer(data=request.data)
    if new_apt.is_valid():
        new_apt.save()
        return HttpResponse(f"New apartment added: {new_apt.data}")


class ApartmentsAPIView(generics.ListAPIView):
    queryset = Apartments.objects.all()
    serializer_class = ApartmentsSerializer
