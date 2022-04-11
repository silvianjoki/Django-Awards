from email.policy import default
import profile
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_pic = models.ImageField(upload_to = 'images/', null=True)
    bio =  models.TextField()
    email = models.EmailField()


    def __str__(self):
        return self.user.username
    
    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete() 

    def edit_bio(self, new_bio):
        self.bio = new_bio
        self.save()

class Project(models.Model):
    name = models.CharField(max_length=30)
    screenshot = models.ImageField(upload_to = 'images/', null=True)
    description = models.TextField()
    link = models.URLField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    voters = models.IntegerField()
    creator_design = models.FloatField(default=0)
    creator_usability = models.FloatField(default=0)
    creator_creativity = models.FloatField(default=0)
    creator_content = models.FloatField(default=0)
    creator_score = models.FloatField(default=0)
    
    def __str__(self):
        return self.name
    
    def save_project(self):
        self.save()
        
    def delete_project(self):
        self.delete()
        
    def voters_count(self):
        return self.voters.count()

    @classmethod
    def display_all_projects(cls):
        return cls.objects.all()
    
    @classmethod
    def get_user_projects(cls, profile):
        return cls.objects.filter(profile=profile)
    
    @classmethod
    def search_project(cls, name):
        return cls.objects.filter(name__icontains = name)
    
class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name = None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, ** kwargs):
        defaults = {'min_value':self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Vote(models.Model):
    post_date = models.DateTimeField(auto_now_add = True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    design = IntegerRangeField(min_value=1, max_value=10)
    usability = IntegerRangeField(min_value=1, max_value=10)
    creativity = IntegerRangeField(min_value=1, max_value=10)
    content = IntegerRangeField(min_value=1, max_value=10)
    
    def save_vote(self):
        self.save()
        
    def delete_vote(self):
        self.delete()
        
    @classmethod
    def get_project_voters(cls, voter):
        return cls.objects.filter(voter=voter)
    @classmethod
    def get_project_votes(cls,project):
        return cls.objects.filter(project=project)
    class Meta:
        ordering = ['-post_date']
    