
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from blog.models import Post
from .forms import NewPostForm


# Create your views here
# region function base
def post_list_view(request):
    posts = Post.objects.filter(status='pub').order_by('-updated_date')
    context = {'posts': posts}
    return render(request , 'blog/posts_lists.html' , context)

def post_detail_view(request , pk):
    posts = get_object_or_404(Post , pk=pk)
    context = {'posts': posts}
    return render(request , 'blog/post_detail.html' , context)


def post_create_view(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = NewPostForm()
    return render(request , 'blog/add_post.html' , context ={'form': form})

def post_update_view(request , pk):
    post = get_object_or_404(Post, pk=pk)
    form =NewPostForm(request.POST or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect('post_list')

    return render(request , 'blog/add_post.html' , {'form':form})

def delete_post_view(request , pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request , 'blog/post_delete.html' , {'post':post})
# endregion

# region Class Base View

class PostListView(generic.ListView):
    template_name = 'blog/posts_lists.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(status='pub').order_by('-updated_date')

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(generic.CreateView):
     form_class = NewPostForm
     template_name = 'blog/add_post.html'

class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = NewPostForm
    template_name = 'blog/add_post.html'


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('post_list')

# endregion