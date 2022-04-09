from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import Profile, Project, Vote
from django.contrib.auth.decorators import login_required
from .forms import CreateProfileForm, RateProjectForm, CreateProjectForm
from .email import send_welcome_email
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth.models import User



# Create your views here.

def create_profile(request):
    current_user = request.user
    title = "Create Profile"
    if request.method == 'POST':
        form = CreateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return HttpResponseRedirect('/')

    else:
        form = CreateProfileForm()
    return render(request, 'user/create_profile.html', {"form": form, "title": title})

def email(request):
    current_user = request.user
    email = current_user.email
    name = current_user.username
    send_welcome_email(name, email)
    return redirect(create_profile)
    
@login_required(login_url='/accounts/login/')
def home(request):
    projects = Project.display_all_projects()
    projects_scores = projects.order_by('-average_score')
    highest_score = None
    highest_votes = None
    if len(projects) >= 1:
        highest_score = projects_scores[0]
        votes = Vote.get_project_votes(highest_score.id)
        highest_votes = votes[:3]   
    
    return render(request, 'home.html', {'projects': projects, 'projects_scores':projects_scores, 'highest_score':highest_score, 'highest_votes':highest_votes})

@login_required(login_url='/accounts/login/')
def profile(request, profile_id):
    try:
        user = User.objects.get(pk = profile_id)
        profile = Profile.objects.get(user = user)
        title = profile.user.username
        projects = Project.get_user_projects(profile.id)
        projects_count = projects.count()
        votes= []
        for project in projects:
            votes.append(project.creator_score)
        total_votes = sum(votes)
        average = 0
        if len(projects)> 1:
            average = total_votes / len(projects)
    except Profile.DoesNotExist:
        raise Http404()    
    return render(request, 'user/profile.html', {'profile':profile, 'title': title, 'projects':projects, 'projects_count':projects_count, 'votes':total_votes, 'average': average})

@login_required(login_url='/accounts/login/')
def project ( request, project_id):
    form = RateProjectForm
    title = project.name.title() + " | slyAwwards"
    project = Project.objects.get(pk = project_id)
    votes = Vote.get_project_votes(project_id)
    total_votes= votes.count()
    voted=False
    
    voters_list =[]
    average_list = []
    design_list = []
    usability_list = []
    creativity_list = []
    content_list = []
    for vote in votes:
        voters_list.append(vote.voter.id)
        average_summation = vote.design + vote.creativity + vote.content + vote.usability
        average = average_summation/3
        average_list.append(average)
        content_list.append(vote.content)
        creativity_list.append(vote.creativity)
        design_list.append(vote.design)
        usability_list.append(vote.usability)
        
        try:
            user = User.objects.get(pk = request.user.id)
            profile = Profile.objects.get(user = user)
            voter = Vote.get_project_voters(profile)
            voted = False
            if request.user.id in voters_list: 
                voted = True
        except Profile.DoesNotExist:
            voted = False
            
        if len(average_list) > 0:
            average_score = sum(average_list) / len(average_list)
            project.average_score = average_score
            project.save()
            
        if total_votes != 0:
            creator_design = sum(design_list) / total_votes
            creator_creativity = sum(creativity_list)/ total_votes
            creator_content = sum(content_list) / total_votes
            creator_usability = sum(usability_list) / total_votes 
            project.creator_design = creator_design
            project.creator_content =creator_content
            project.creator_usability = creator_usability
            project.creator_creativity = creator_creativity
            project.save() 
        
    return render(request, 'project/project.html', {'title':title, 'form':form, 'project':project, 'votes':votes, 'total_votes':total_votes, 'voted':voted})
