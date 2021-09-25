from django.db import models
import uuid
from users.models import Profile

UP_VOTE = 'up'
DOWN_VOTE = 'down'


class BaseModelMixin(models.Model):
    """
        Base model mixin to create 'created' and 'id' field for all models
    """
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        abstract = True


class Project(BaseModelMixin, models.Model):
    """
        Project Model, to store information related to each project
    """
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)

    @property
    def reviewers(self):
        """Getting all reviewers that voted this project"""
        return self.review_set.all().values_list('owner__id', flat=True)

    @property
    def get_vote_count(self):
        """getting total number of votes"""
        reviews = self.review_set.all()
        up_votes = reviews.filter(value=UP_VOTE).count()
        total_votes = reviews.count()

        ration = (up_votes / total_votes) * 100
        self.vote_total = total_votes
        self.vote_ratio = ration
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-vote_ratio', '-vote_total', 'title')


class Review(BaseModelMixin, models.Model):
    """
        Review model, to store project reviews
    """

    VOTE_TYPE = (
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
    )

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)

    def __str__(self):
        return self.value

    class Meta:
        unique_together = [['owner', 'project']]


class Tag(BaseModelMixin, models.Model):
    """
        Tag model, to store project tags
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
