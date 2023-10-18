from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import PostForm
from .models import Post


# Create your views here.
def index(request):
    if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                # 이미지 및 GIF가 없으면 글을 작성하지 않음
                if not post.image and not post.gif:
                    form.add_error(None, "이미지 또는 GIF를 업로드해야 합니다.")
                else:
                    form.save()
                    return redirect('/image_list')  # 글 목록 페이지로 리다이렉트
    else:
        form = PostForm()   
    return render(request, 'img/index.html', {'form': form})
  


def image_list(request):
    # 이미지 및 GIF 파일 목록 가져오기
    image_posts = Post.objects.filter(image__isnull=False)
    gif_posts = Post.objects.filter(gif__isnull=True)
    return render(request, 'img/image_list.html', {'image_posts': image_posts, 'gif_posts': gif_posts})