from django.db.models import Q
from django.shortcuts import redirect, render
from .models import Post, Comment
from users.models import Profile
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator

# Create your views here.


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            return Post.objects.get_queryset().filter(Q(content__icontains = q) | Q(title__icontains = q))
        return super().get_queryset()

class PostDetailView(DetailView):
    model = Post
    context_object_name='post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        comments = Comment.objects.all().filter(post__id = self.get_object().id).order_by('-date_posted')
        context['comments'] = comments
        return context

    def post(self, request, **kwargs):
        #save the comment
        body = request.POST.get('body')
        Comment.objects.create(author = request.user, post = self.get_object(), body = body)
        return redirect('post-detail', self.get_object().id)
    
    

class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        user = self.get_object().author
        return self.request.user == user

class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        user = self.get_object().author
        return self.request.user == user


def user_posts(request, username):
    author = User.objects.all().filter(username = username).get()
    posts = Post.objects.all().filter(author=author).order_by('-date_posted')

    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'user': author
    }
    return render(request, 'blog/user-page.html', context)
    

def about(request):
    context = { 'title': 'About'}
    return render(request, 'blog/about.html', context)