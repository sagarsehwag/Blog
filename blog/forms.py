from django import forms
from .models import BlogPost, PostComment


class BlogPostForm(forms.ModelForm):

    class Meta():
        model = BlogPost
        fields = ('title', 'author', 'text')

        widgets = {
            'title': forms.TextInput(attrs={'class': '',
                                            'placeholder': 'Write title here..'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea poscontent',
                                          'placeholder': 'Write text here..'})
        }


class PostCommentForm(forms.ModelForm):

    class Meta():
        model = PostComment
        fields = ('author', 'text')

        widgets = {
            'author': forms.TextInput(attrs={'class': '',
                                             'placeholder': 'Author'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea',
                                          'placeholder': 'Write text here..'})
        }
