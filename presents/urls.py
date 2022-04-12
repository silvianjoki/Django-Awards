
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django_registration.backends.one_step.views import RegistrationView

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    re_path('^$', views.home, name = 'home'),
    path ('email/', views.email, name = 'email'),
    path('create_profile/', views.create_profile, name = 'create_profile'),
    path('profile/', views.profile, name='profile'),
    path('project/', views.project, name='project'),
    path('add_project/', views.add_project, name='add_project'),
    path('search_project/', views.search_project, name= 'search_project'),
    path('rate_project/', views.rate_project, name ='rate_project'),
    re_path(r'^api/projects/$', views.ProjectList.as_view()),
    re_path(r'^api/profiles/$', views.ProfileList.as_view()),
    
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/',
        RegistrationView.as_view(success_url=reverse_lazy('home')),
        name='django_registration_register'),

    re_path('^logout/$', auth_views.LogoutView.as_view(), name='logout'), 
    re_path('^login/$', LoginView.as_view(), {"next_page": '/'}),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)