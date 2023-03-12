from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, User
from datetime import datetime
from .filters import PostFilter
from .forms import PostFormCreate_and_Update, UserFormUpdate, UserPasswordChange
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group


class PostList(ListView):
    model = Post
    ordering = '-date_of_creation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now_time'] = datetime.now()
        context['is_not_author'] = not self.request.user.groups.filter(name='Authors').exists()
        return context


class PostListSearch(ListView):
    model = Post
    ordering = '-date_of_creation'
    template_name = 'post_search.html'
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


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post',)
    form_class = PostFormCreate_and_Update
    model = Post
    template_name = 'post_create.html'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post', )
    form_class = PostFormCreate_and_Update
    model = Post
    template_name = 'post_update.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsPortal.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class UserUpdate(UpdateView):
    form_class = UserFormUpdate
    model = User
    template_name = 'UserUpdate.html'
    success_url = reverse_lazy('post_list')


def logout_user(request):
    logout(request)
    return redirect('post_list')


def add_author(request):
    user = request.user
    authors_group = Group.objects.get(name='Authors')
    common_group = Group.objects.get(name='Common')
    if not request.user.groups.filter(name='Authors').exists():
        authors_group.user_set.add(user)
        common_group.user_set.remove(user)
    return redirect('post_list')


class User_password_change(PasswordChangeView):
    form_class = UserPasswordChange
    template_name = 'user_password_change.html'
    success_url = reverse_lazy('post_list')

