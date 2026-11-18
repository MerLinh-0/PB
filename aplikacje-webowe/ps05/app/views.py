from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from app.forms import ExperimentForm
from app.models import Experiment, Project


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
        
    return render(request, 'registration/register.html', {'form': form})


def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})


def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    experiments = project.experiment_set.all()
    return render(request, 'projects/project_detail.html', {'project': project, 'experiments': experiments})


def experiment_detail(request, id):
    experiment = get_object_or_404(Experiment, id=id)
    return render(request, 'projects/experiment_detail.html', {'experiment': experiment})

@login_required
def experiment_create(request):
    if request.method == 'POST':
        form = ExperimentForm(request.POST)
        if form.is_valid():
            experiment = form.save(commit=False)
            experiment.created_by = request.user
            experiment.save()
            return redirect('experiment_detail', id=experiment.id)
    else:
        form = ExperimentForm()

    return render(request, 'projects/experiment_form.html', {'form': form})

@login_required
def experiment_edit(request, id):
    experiment = get_object_or_404(Experiment, id=id)
    if experiment.created_by != request.user:
        messages.error(request, "Nie masz uprawnień do edycji tego eksperymentu.")
        return redirect('project_list')

    if request.method == 'POST':
        form = ExperimentForm(request.POST, instance=experiment)
        if form.is_valid():
            form.save()
            messages.success(request, "Eksperyment został zaktualizowany.")
            return redirect('experiment_detail', id=experiment.id)
    else:
        form = ExperimentForm(instance=experiment)
        
    return render(request, 'projects/experiment_form.html', {'form': form, 'is_edit': True, 'experiment': experiment})

@login_required
def experiment_delete(request, id):
    experiment = get_object_or_404(Experiment, id=id)
    if experiment.created_by != request.user:
        messages.error(request, "Nie masz uprawnień do usunięcia tego eksperymentu.")
        return redirect('project_list')

    if request.method == 'POST':
        experiment.delete()
        messages.success(request, "Eksperyment został usunięty.")
        return redirect('project_detail', id=experiment.project.id)
        
    return render(request, 'projects/experiment_confirm_delete.html', {'experiment': experiment})
