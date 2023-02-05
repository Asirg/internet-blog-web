from datetime import datetime
from django.utils.timezone import now
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Count

# Create your models here.

class Tag(models.Model):
    name = models.CharField("Name", max_length=150)
    url = models.SlugField("url", max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

class Category(models.Model):
    parent = models.ForeignKey(
        to="self", verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True, related_name="childs"
    )
    
    name = models.CharField("Name", max_length=150)
    cover = models.ImageField("Poster", upload_to="category/", null=True, blank=True)
    url = models.SlugField("url", unique=True)

    def __str__(self):
        return self.name

    @property
    def get_popular_tags(self):
        posts = Post.objects.filter(categories__in = self.get_sub_categories).distinct()
        tags_count = Post.objects\
                    .filter(id__in = posts)\
                    .values("tags__name")\
                    .annotate(Count("tags__name"))\
                    .order_by("-tags__name__count")
        return tags_count

    @property
    def get_sub_categories(self):
        return [self] if self.parent else self.childs.all() 

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Post(models.Model):
    author = models.ForeignKey(
        to=get_user_model(), verbose_name="Author", on_delete=models.CASCADE, related_name='posts'
    )
    tags = models.ManyToManyField(
        to=Tag, verbose_name="Tags", related_name="post_tag", blank=True
    )
    categories = models.ManyToManyField(
        to=Category, verbose_name="Categories", related_name="post_category"
    )

    header = models.CharField("Header", max_length=80)
    describe = models.CharField("Describe", max_length=180)
    cover = models.ImageField("Cover", upload_to="post/")
    content = models.TextField("Content")
    number_of_views = models.PositiveIntegerField("Number of views", default=0)
    publication_date = models.DateTimeField("Publication date", default=now)
    is_raw = models.BooleanField("Is raw?")

    @property
    def get_comments(self):
        return self.comment_set.filter(parent__isnull=True)

    @property
    def like_count(self):
        return self.reactions.filter(like=True).count()

    @property
    def dislike_count(self):
        return self.reactions.filter(like=False).count()

    @property
    def comment_count(self):
        return self.comment_set.all().count()

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

class Comment(models.Model):
    author = models.ForeignKey(
        to=get_user_model(), verbose_name="Author", on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        to=Post, verbose_name="Post", on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        to="self", verbose_name="Parent", on_delete=models.CASCADE, blank=True, null=True, related_name="childs"
    )

    content = models.TextField("Content")
    date = models.DateTimeField('date', default=now)

    @property
    def get_childs(self):
        return self.childs.all().order_by("date")

    def __str__(self):
        return f"{self.id}:{self.author}:{self.post}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-id']

class Reaction(models.Model):
    author = models.ForeignKey(
        to=get_user_model(), verbose_name="Author", on_delete=models.CASCADE, related_name='reactions'
    )
    post = models.ForeignKey(
        to=Post, verbose_name="Post", on_delete=models.CASCADE, blank=True, null=True, related_name='reactions'
    )
    comment = models.ForeignKey(
        to=Comment, verbose_name="Comment", on_delete=models.CASCADE, blank=True, null=True, related_name='reactions'
    )

    like = models.BooleanField("Is like?")

    def __str__(self):
        return f"{self.author}:{self.post}={self.like}"

    class Meta:
        verbose_name = "Reaction"
        verbose_name_plural = "Reactions"