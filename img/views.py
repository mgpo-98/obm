from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .models import Image, Hashtag
from .forms import ImageUploadForm

# Create your views here.

def index(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            hashtags = form.cleaned_data.get('hashtags', '').split()
            image.save()
            for tag in hashtags:
                tag = tag.strip('#')
                hashtag, created = Hashtag.objects.get_or_create(name=tag)
                image.hashtags.add(hashtag)

            image.save()
            return redirect('img:image_list')

    else:
        form = ImageUploadForm()
    context = {
        'form': form,
    }
    return render(request, 'img/index.html', context)


def image_list(request):
    image_items = Image.objects.all()
    return render(request, 'img/image_list.html', {'image_items': image_items})


def search_images(request):
    search_query = request.GET.get('search')
    images = Image.objects.filter(hashtags__name__icontains=search_query)  # 검색어를 포함하는 이미지를 필터링
    return render(request, 'img/search_results.html', {'images': images, 'search_query': search_query})