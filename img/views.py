from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .models import Image, Hashtag, SearchHistory
from .forms import ImageUploadForm
from django.http import JsonResponse
# Create your views here.

def index(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            hashtags = form.cleaned_data.get('hashtags', '').split()
            image.save()
            for tag in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(name=tag)
                image.hashtags.add(hashtag)
                data = {'message': '업로드가 성공적으로 완료되었습니다.'}  # JSON 응답 데이터
               

            
            return JsonResponse({'success': 'Image uploaded successfully!'})

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
    query = request.GET.get('search')
    if query:
        # 검색 내역 저장
        SearchHistory.objects.create(query=query)
        results = YourModel.objects.filter(title__icontains=query)
    else:
        results = YourModel.objects.all()
    images = Image.objects.filter(hashtags__name__icontains=query)  # 검색어를 포함하는 이미지를 필터링
    return render(request, 'img/search_results.html', {'images': images, 'query': query})


