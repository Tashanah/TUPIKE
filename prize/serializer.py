from rest_framework import serializers
from .models import Profile, Projects

class MerchSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoringaMerch
        fields = ('name', 'description', 'price')