from rest_framework import serializers

from apartments.models import Apartments


class ApartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartments
        fields = "__all__"
        read_only_fields = ["id"]
