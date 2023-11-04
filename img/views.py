from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .models import Image, Hashtag, SearchHistory
from .forms import ImageUploadForm
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count
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

# def get_search_ranking(request):
#     query = request.GET.get('search')
#     search_history = SearchHistory.objects.values('query').annotate(search_count=models.Count('query')).order_by('-search_count')[:10]
#     return render(request, 'img/image_list.html', {'search_history': search_history, 'query': query})

def get_search_ranking():
    ranking = SearchHistory.objects.values('query').annotate(search_count=Count('query')).order_by('-search_count')
    return ranking

def image_list(request):
    image_items = Image.objects.all()
    search_ranking = get_search_ranking()
    return render(request, 'img/image_list.html', {'image_items': image_items,'search_ranking': search_ranking})


def search_images(request):
    query = request.GET.get('search')
    if query:
        # 검색 내역 저장
        current_time = timezone.now()
        SearchHistory.objects.create(query=query, search_time=current_time)
        results = Hashtag.objects.filter(name__icontains=query)
    else:
        results = Hashtag.objects.all()
    images = Image.objects.filter(hashtags__name__icontains=query)  # 검색어를 포함하는 이미지를 필터링
    return render(request, 'img/search_results.html', {'images': images, 'query': query})


