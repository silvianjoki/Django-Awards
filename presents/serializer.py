from rest_framework import serializers
from .models import Profile, Project

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'profile_pic', 'bio', 'location', 'email', 'link' )

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'screenshot', 'description', 'link', 'profile', 'voters','post_date', 
                'creator_design', 'creator_usability', 'creator_creativity', 'creator_content', 'creator_score' )

