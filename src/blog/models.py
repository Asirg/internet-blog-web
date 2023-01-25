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
    cover = models.ImageField("Poster", upload_to="category/")
    url = models.SlugField("url", unique=True)

    def __str__(self):
        return self.name

    @property
    def get_popular_tags(self):
        tags = Post.objects.filter(categories__in = [self]).values("tags__name").annotate(Count("tags__name"))
        return tags

    @property
    def get_sub_categories(self):
        return [
            self.id, * [child["id"] for child in self.childs.all().values("id")]
        ]

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Post(models.Model):
    author = models.ForeignKey(
        to=get_user_model(), verbose_name="Author", on_delete=models.CASCADE
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

    def __str__(self):
        return self.header

    def get_comment(self):
        return self.comment_set.filter(parent__isnull=True)

    @property
    def like_count(self):
        return self.reaction_set.filter(like=True).count()

    @property
    def dislike_count(self):
        return self.reaction_set.filter(like=False).count()

    @property
    def comment_count(self):
        return self.comment_set.all().count()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

class Comment(models.Model):
    author = models.ForeignKey(
        to=get_user_model(), verbose_name="Author", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        to=Post, verbose_name="Post", on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        to="self", verbose_name="Parent", on_delete=models.CASCADE, blank=True, null=True
    )

    content = models.TextField("Content")

    def __str__(self):
        return f"{self.id}:{self.author}:{self.post}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-id']

class Reaction(models.Model):
    author = models.ForeignKey(
        to=get_user_model(), verbose_name="Author", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        to=Post, verbose_name="Post", on_delete=models.CASCADE, blank=True, null=True
    )
    comment = models.ForeignKey(
        to=Comment, verbose_name="Comment", on_delete=models.CASCADE, blank=True, null=True
    )

    like = models.BooleanField("Is like?")

    def __str__(self):
        return f"{self.author}:{self.post}={self.like}"

    class Meta:
        verbose_name = "Reaction"
        verbose_name_plural = "Reactions"