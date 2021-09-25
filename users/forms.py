from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile, Skill, Message

User = get_user_model()


class StyleFormMixin:
    """Mixin to style fields input"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'input'})


class CustomerUserCreationForm(StyleFormMixin, UserCreationForm):
    """
        Custom user creation form
    """

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }


class ProfileForm(StyleFormMixin, ModelForm):
    """
        Model Form to edit profile
    """

    class Meta:
        model = Profile
        fields = ['name', 'username', 'email', 'location', 'short_intro', 'bio',
                  'profile_image', 'social_github', 'social_linkedin', 'social_twitter',
                  'social_youtube', 'social_website']


class SkillForm(StyleFormMixin, ModelForm):
    """
        Model form to Create and Edit Skill
    """

    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']


class MessageForm(StyleFormMixin, ModelForm):
    """
        Model form to Create Message
    """

    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']
