from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings
from .utils import search_profile, paginate_profiles
from .models import Profile, Skill, Message
from .forms import CustomerUserCreationForm, ProfileForm, SkillForm, MessageForm

User = get_user_model()


def login_view(request):
    """Temporary view to login the user"""
    context = {'page': 'login'}
    if request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']
        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if 'next' in request.GET:
                    return redirect(request.GET['next'])
                return redirect('account')
            else:
                messages.error(request, 'The credentials are wrong!')
        else:
            messages.error(request, 'This user does not exist!')
    return render(request, 'users/login_register.html', context)


def logout_view(request):
    """View to Logout """
    logout(request)
    messages.info(request, 'User was successfully logged out!')
    return redirect('login')


def register_user(request):
    """View to register users"""
    if request.method == 'POST':
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'user account was successfully created')
            login(request, user)
            return redirect('edit_account')
    else:
        form = CustomerUserCreationForm()

    context = {'page': 'register', 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    """Renders all profiles"""
    profiles_, search_query = search_profile(request)
    profiles_, custom_range = paginate_profiles(request,
                                                profiles_,
                                                settings.PROFILE_PER_PAGE)

    return render(request, 'users/profiles.html', {'profiles': profiles_,
                                                   'custom_range': custom_range,
                                                   'search_query': search_query})


def user_profile(request, username):
    """Render user profile"""
    profile = get_object_or_404(Profile, user__username=username)
    top_skills = profile.skill_set.exclude(description__exact='')
    other_skills = profile.skill_set.filter(description='')
    context = {'profile': profile,
               'top_skills': top_skills,
               'other_skills': other_skills}
    return render(request, 'users/user-profile.html', context)


@login_required
def user_account(request):
    """Render user account"""
    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'users/account.html', context)


@login_required
def edit_account(request):
    """View to edit user profile"""
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(instance=profile,
                           data=request.POST,
                           files=request.FILES)

        if form.is_valid():
            form.save()
            return redirect('account')
        else:
            messages.error(request, form.errors)
    else:
        form = ProfileForm(instance=profile)

    context = {'form': form}

    return render(request, 'users/profile_form.html', context)


@login_required
def create_skill(request):
    """View to create a skill"""
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user.profile
            skill.save()
            messages.success(request, 'Skill was created successfully')
            return redirect('account')
        else:
            messages.error(request, form.errors)
    else:
        form = SkillForm()

    context = {"form": form}
    return render(request, 'users/skill_form.html', context)


@login_required
def update_skill(request, pk):
    """View to update a skill"""
    profile = request.user.profile
    skill = get_object_or_404(Skill, id=pk, owner=profile)
    if request.method == 'POST':
        form = SkillForm(instance=skill, data=request.POST)
        if form.is_valid():
            skill.save()
            messages.success(request, 'Skill was updated successfully')
            return redirect('account')
        else:
            messages.error(request, form.errors)
    else:
        form = SkillForm(instance=skill)

    context = {"form": form}
    return render(request, 'users/skill_form.html', context)


@login_required
def delete_skill(request, pk):
    """View to delete the skill"""
    profile = request.user.profile
    skill = get_object_or_404(Skill, id=pk, owner=profile)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully')
        return redirect('account')
    return render(request, 'delete_object.html', context={'object': skill})


@login_required
def inbox(request):
    """View to show messages of each user"""
    profile = request.user.profile
    inbox_messages = profile.messages.all()
    unread_messages = profile.messages.filter(is_read=False).count()
    context = {'inbox_messages': inbox_messages, 'unread_messages': unread_messages}
    return render(request, 'users/inbox.html', context)


@login_required
def view_message(request, pk):
    """View to see messages"""
    message = get_object_or_404(Message,
                                id=pk,
                                recipient=request.user.profile)
    message.is_read = True
    message.save()
    return render(request, 'users/message.html', {'message': message})


def send_message(request, pk):
    """Send message to a user"""
    profile = get_object_or_404(Profile, id=pk)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            if request.user.is_authenticated:
                message.sender = request.user.profile
            message.recipient = profile
            message.save()
            messages.success(request,'Message was successfully sent!')
            return redirect('user_profile', profile.user.username)
        else:
            messages.error(request, form.errors)
    else:
        form = MessageForm()

    context = {'profile': profile, 'form': form}
    return render(request, 'users/message_form.html', context)
