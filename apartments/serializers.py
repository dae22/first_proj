from rest_framework import serializers

from apartments.models import Apartments


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartments
        fields = ["id", "description", "price"]
        read_only_fields = ["id"]
