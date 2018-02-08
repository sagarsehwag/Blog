from django.db import models
from django.utils import timezone
from django.urls import reverse, reverse_lazy

# Create your models here.


class BlogPost(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.CharField(max_length=4096)
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(default=create_date)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def last_updated(self):
        self.last_updated = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class PostComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE,
                             related_name='comments')
    author = models.CharField(max_length=256)
    text = models.CharField(max_length=2048)
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.post.pk})

    def __str__(self):
        self.text
