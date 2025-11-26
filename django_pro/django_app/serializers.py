from rest_framework import serializers
from .models import DjangoAppCloudtable

class CloudTableSerializer(serializers.ModelSerializer):
    class Meta:
        model=DjangoAppCloudtable
        fields="__all__"

