from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import Profile, Project, Vote
from django.contrib.auth.decorators import login_required
from .forms import CreateProfileForm, RateProjectForm, CreateProjectForm
from .email import send_signup_email





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
    send_signup_email(name, email)
    return redirect(create_profile)
    