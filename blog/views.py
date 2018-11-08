from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .models import Articleupload
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from tablib import Dataset

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_details.html', {'post' : post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

#def post_draft_list(request):


def simple_upload(request):
    if request.method == 'POST':
        articleupload_resource = ArticluploadResource()
        dataset = Dataset()
        new_articleupload = request.FILES['myfile']

        imported_data = dataset.load(new_articleupload.read())
        result = articleupload_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            articleupload_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'blog/simple_upload.html')

def news(request):
    articles = Articleupload.objects.filter(postdate__lte=timezone.now()).order_by('postdate')
    return render(request, 'blog/news.html', {'articles': articles})

def news_detail(request, pk):
    articles = get_object_or_404(Articleupload, pk=pk)
    return render(request, 'blog/news_details.html', {'articles': articles})

