from django.shortcuts import render
from django.views.generic import ListView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = 'heading'
    template_name = 'post.html'
    context_object_name = 'post'
