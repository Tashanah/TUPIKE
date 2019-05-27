from rest_framework import serializers
from .models import Profile, Projects

class MerchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profile_photo', 'bio', 'profile_name', 'user')