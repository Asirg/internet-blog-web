from datetime import date

from django.db import models
from django.contrib.auth import get_user_model

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
        to="self", verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True
    )
    
    name = models.CharField("Name", max_length=150)
    cover = models.ImageField("Poster", upload_to="category/")
    url = models.SlugField("url", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categoriess"

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

    header = models.CharField("Header", max_length=150)
    describe = models.CharField("Describe", max_length=400)
    cover = models.ImageField("Cover", upload_to="post/")
    content = models.TextField("Content")
    number_of_views = models.PositiveIntegerField("Number of views", default=0)
    publication_date = models.DateField("Publication date", default=date.today)
    is_raw = models.BooleanField("Is raw?")

    def __str__(self):
        return self.header

    def get_comment(self):
        return self.comment_set.filter(parent__isnull=True)

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