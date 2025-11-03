from rest_framework import serializers
from .models import CloudTable

class CloudTableSerializer(serializers.ModelSerializer):
    class Meta:
        model=CloudTable
        fields="__all__"

