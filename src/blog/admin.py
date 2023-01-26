from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from blog.models import Tag, Category, Post, Comment, Reaction

class TagInLines(admin.TabularInline):
    model = Tag
    extra = 1

class CategoryInLines(admin.TabularInline):
    model = Category
    extra = 1

class CommentInLines(admin.TabularInline):
    model = Comment
    extra = 1
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url", )
    list_display_links = ("name", "url", )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url", "parent",)
    list_display_links = ("name", "url", )

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(
				widget=CKEditorUploadingWidget(),
				label="Content"
		)

    class Meta:
        model = Post
        fields = '__all__'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "header", "author", "display_categories",  "publication_date", "is_raw", )
    list_display_links = ("header", )
    list_editable = ("is_raw", )
    fieldsets = (
        (None, 
            {
                "fields":(("author", "header", "cover", "is_raw", ), )
        }),
        ("Classification", 
            {
                "fields":(("categories", "tags", ), )
        }),
        ("Content", 
            {
                "fields":(("content", "describe",  ), )
        }),
        ("option",
            {
                "classes": ("collapse", ),
                "fields":("number_of_views", "publication_date")
        }),
    )
    readonly_fields = ("number_of_views", "publication_date", )

    inlines = (CommentInLines, )
    form = PostAdminForm

    list_filter = ("categories", "tags", )
    search_fields = ("header", "author__username", )
    save_on_top = True
    save_as = True

    def display_categories(self, obj):
        return ",".join([val[0] for val in list(obj.categories.values_list("name"))])


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author", )

    inlines = (CommentInLines, )

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "like", "author", )