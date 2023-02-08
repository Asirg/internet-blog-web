from django import forms

from blog.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('number_of_views', 'publication_date', )