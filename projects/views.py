from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .forms import ProjectForm, ReviewForm
from .models import Project
from .utils import search_project, paginate_projects


def projects(request):
    """View to render all projects"""
    total_projects, search_query = search_project(request)
    total_projects, custom_range = paginate_projects(request,
                                                     total_projects,
                                                     settings.PROJECT_PER_PAGE)
    context = {'projects': total_projects,
               'search_query': search_query,
               'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    """View to render a project"""
    project_object = get_object_or_404(Project, id=pk)
    profile = request.user.is_authenticated and request.user.profile
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = profile
            review.project = project_object
            review.save()
            project_object.get_vote_count
            messages.success(request, 'Your review was successfully saved')
        else:
            messages.error(request, form.errors)

    else:
        form = ReviewForm()

    return render(request, 'projects/single-project.html', {'project': project_object,
                                                            'form': form})


@login_required
def create_project(request):
    """View to create a project"""
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, files=request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context=context)


@login_required
def update_project(request, pk):
    """View to update the project"""
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(instance=project,
                           data=request.POST,
                           files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context=context)


@login_required
def delete_project(request, pk):
    """View to delete the project"""
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    return render(request,
                  'delete_object.html',
                  context={'object': project})
