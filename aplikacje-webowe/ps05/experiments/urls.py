from app import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/projects/', permanent=False), name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:id>', views.project_detail, name='project_detail'),
    path('experiments/<int:id>/', views.experiment_detail, name='experiment_detail'),
    path('experiments/add/', views.experiment_create, name='experiment_create'),
    path('experiments/<int:id>/edit/', views.experiment_edit, name='experiment_edit'),
    path('experiments/<int:id>/delete/', views.experiment_delete, name='experiment_delete')
]
