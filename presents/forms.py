from django import forms
from .models import Project, Profile, Vote
from django.forms import ModelForm

class CreateProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        
class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['profile', 'voters', 'post_date', 
                'design_score', 'usability_score', 'creativity_score', 'content_score'
                'creator_design', 'creator_usability', 'creator_creativity', 'creator_content', 'creator_score']
        
class RateProjectForm(ModelForm):
    class Meta:
        model: Vote
        exclude = ['post_date', 'voter', 'project']
