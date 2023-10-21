from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .models import Image, Hashtag
from .forms import ImageUploadForm

# Create your views here.

def index(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST)
        image_form  = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid() and image_form.is_valid() :
            post = form.save()
            content = form.cleaned_data['content']
            hashtags = [tag.strip('#') for tag in content.split() if tag.startswith('#')][:7]  # 최대 7개 해시태그
            for tag in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(name=tag)
                post.hashtags.add(hashtag)
            post.save()
            image_form.instance.post = post  # 이미지와 게시물을 연결
            image_form.save()
            return redirect('image_list')
    else:
        form = ImageUploadForm()
        image_form = ImageUploadForm()
    context = {
        'form': form,
        'image_form': image_form
    }
    return render(request, 'img/index.html', context)


def image_list(request):
    image_items = Image.objects.all()
    return render(request, 'img/image_list.html', {'image_items': image_items})