from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Project, IntegerRangeField, Vote
# Create your tests here.

class ProfileTestCase(TestCase):
    # Set up method
    def setUp(self):
        self.silvia= User(username = 'silvia',  email ='silvia@gmail.com', password= '1234')
        self.profile = Profile(user = self.silvia, profile_pic='mypicture', bio='bio', location= 'nairobi', email='silvia@gmail.com', link = 'www.profile.com')
        self.silvia.save()
        self.profile.save_profile()

    def test_instance(self):
        self.assertTrue(isinstance(self.silvia,User))
        self.assertTrue(isinstance(self.silvia,Profile))

    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()
        

class ProjectTestCase(TestCase):
    def setUp(self):
        self.silvia = User(username = 'silvia',  email ='silvia@gmail.com', password= '1234')
        self.profile = Profile(user = self.silvia, profile_pic='mypicture', bio='bio', location= 'nairobi', email='silvia@gmail.com', link = 'www.profile.com')
        self.project = Project(name='testing', screenshot ='screenshoturl', description='sample project', link='testlink', profile=self.profile)
        
        self.silvia.save()
        self.profile.save_profile
        self.project.save_project
        
    def tearDown(self):
        User.objects.all().delete()
        Profile.objects.all().delete()
        Project.objects.all().delete()
        
    def test_save_project(self):
        projects = Project.objects.all()
        self.assertTrue(len(projects)>0)
        
    def test_image_instance(self):
        self.assertTrue(isinstance(self.project, Project))
    
    def test_delete_project(self):
        projects1 = Project.objects.all()
        self.assertEqual(len(projects1),1)
        self.project.delete_project()
        projects2 = Project.objects.all()
        self.assertEqual(len(projects2),0)

    def test_search_projects(self):
        project = Project.search_project('testing')
        self.assertEqual(len(project),1)
    
    def test_display_projects(self):
        projects = Project.display_all_projects()
        self.assertTrue(len(projects) > 0) 
    
    def test_get_user_projects_(self):
        profile_projects = Project.get_user_projects(self.profile.id)
        self.assertEqual(profile_projects[0].name, 'testing')
        self.assertEqual(len(profile_projects),1 )
        

class VoteTestCase(TestCase):
    def setUp(self):
        self.silvia = User(username = 'silvia',  email ='silvia@gmail.com', password= '1234')
        self.profile = Profile(user = self.silvia, profile_pic='mypicture', bio='bio', location= 'nairobi', email='silvia@gmail.com', link = 'www.profile.com')
        self.project = Project(name='testing', screenshot ='screenshoturl', description='sample project', link='testlink', profile=self.profile)
        self.vote = Vote(voter=self.profile, project=self.project, design=9, usability= 4, creativity=6, content = 3)
        
        self.silvia.save()
        self.profile.save_profile
        self.project.save_project
        
    def tearDown(self):
        User.objects.all().delete()
        Profile.objects.all().delete()
        Project.objects.all().delete()
        Vote.objects.all().delete()
    
    def test_vote_instance(self):
        self.assertTrue(isinstance(self.vote, Vote))
        
    def test_save_vote(self):
        votes = Vote.objects.all()
        self.assertTrue(len(votes)>0)
        
    def test_delete_vote(self):
        votes1 = Vote.objects.all()
        self.assertEqual(len(votes1),1)
        self.vote.delete_vote()
        votes2 = Project.objects.all()
        self.assertEqual(len(votes2),0)
        
    def test_get_project_votes(self):
        votes = Vote.get_project_votes(self.project)
        self.assertEqual(votes[0].design, 7)
        self.assertEqual(len(votes), 1)
        
    def test_get_project_voters(self):
        voters = Vote.get_project_voters(self.profile)
        self.assertEqual(voters[0].voter.user.username, 'silvia')
        self.assertEqual(len(voters), 1)