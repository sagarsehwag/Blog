from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.views.generic import View, TemplateView, CreateView, UpdateView, DeleteView, RedirectView, ListView, DetailView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .forms import BlogPostForm, PostCommentForm
from .models import PostComment, BlogPost

# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = BlogPost
    context_object_name = "post_list"
    template_name = "blog/post_list.html"

    def get_queryset(self):
        return BlogPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = BlogPost
    context_object_name = "post"
    template_name = "post_detail.html"


class CreatePostView(CreateView, LoginRequiredMixin):
    login_url = '/login'
    redirect_field_name = 'blog/post_detail.html'
    model = BlogPost
    form_class = BlogPostForm
    template_name = "post_form.html"


class PostUpdateView(UpdateView):
    login_url = '/login'
    redirect_field_name = 'blog/post_detail.html'
    model = BlogPost
    form_class = BlogPostForm
    template_name = "post_form.html"


class PostDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('post_list')
    model = BlogPost
    template_name = "post_confirm_delete.html"


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    redirect_field_name = 'blog/post_list.html'
    model = BlogPost
    template_name = "post_drafts.html"
    context_object_name = "posts"

    def get_queryset(self):
        return BlogPost.objects.filter(published_date__isnull=True)


###################################################################################################
@login_required
def post_publish(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

def add_comment(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = PostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostCommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approval(request, pk):
    comment = get_object_or_404(PostComment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(PostComment, pk=pk)
    post_pk = pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
