from contextlib import nullcontext
from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100, null=False)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        if len(self.content) > 200:
            return self.content[0:200] + '...'
        return self.content

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})