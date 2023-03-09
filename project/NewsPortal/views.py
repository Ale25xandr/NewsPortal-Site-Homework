from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, User
from datetime import datetime
from .filters import PostFilter
from .forms import PostFormCreate_and_Update, UserFormUpdate, UserPasswordChange, RegisterUserForm, \
    UserAuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class PostList(ListView):
    model = Post
    ordering = '-date_of_creation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now_time'] = datetime.now()
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


class PostCreate(LoginRequiredMixin, CreateView):
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


class LoginUser(LoginView):
    form_class = UserAuthenticationForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('post_list')


def logout_user(request):
    logout(request)
    return redirect('post_list')


class User_password_change(PasswordChangeView):
    form_class = UserPasswordChange
    template_name = 'user_password_change.html'
    success_url = reverse_lazy('post_list')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'user_register.html'
    success_url = reverse_lazy('post_list')
