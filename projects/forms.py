from django import forms
from .models import Project, Review


class StyleInputMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'input'})


class ProjectForm(StyleInputMixin, forms.ModelForm):
    """Form to handle projects"""

    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link',
                  'source_link', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }


class ReviewForm(StyleInputMixin, forms.ModelForm):
    """Form to create a reivew"""

    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add your comment'
        }
