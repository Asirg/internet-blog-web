from django import forms

from blog.models import Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class PostForm(forms.ModelForm):
    # content = forms.CharField(
    #     widget=CKEditorUploadingWidget(),
    #     label='content'
    # )
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('number_of_views', 'publication_date', )