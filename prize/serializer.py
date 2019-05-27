from rest_framework import serializers
from .models import Profile, Projects

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profile_photo', 'bio', 'profile_name', 'user')

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('profile', 'title', 'image_landing', 'description', 'link')