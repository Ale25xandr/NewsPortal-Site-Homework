from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, User
from datetime import datetime
from .filters import PostFilter
from .forms import PostFormCreate_and_Update, UserFormUpdate
from django.urls import reverse_lazy
# from django.contrib.auth.mixins import LoginRequiredMixin


class PostList(ListView):
    model = Post
    ordering = '-date_of_creation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now_time'] = datetime.now()
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    form_class = PostFormCreate_and_Update
    model = Post
    template_name = 'post_create.html'


class PostUpdate(UpdateView):
    form_class = PostFormCreate_and_Update
    model = Post
    template_name = 'post_update.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class UserUpdate(UpdateView):
    form_class = UserFormUpdate
    model = User
    template_name = 'UserUpdate.html'
    success_url = reverse_lazy('post_list')
