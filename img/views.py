from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .models import Image, Hashtag, SearchHistory
from .forms import ImageUploadForm
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from . import ai_utils
from googletrans import Translator

# Create your views here.

def index(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            hashtags = [tag.replace('"', '').replace(',', '') for tag in form.cleaned_data.get('hashtags', '').split()]
            
            image.save()
            for tag in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(name=tag)
                image.hashtags.add(hashtag)
                data = {'message': '업로드가 성공적으로 완료되었습니다.'}  # JSON 응답 데이터

            return JsonResponse({'success': 'Image uploaded successfully!'})
        else:
            error_message = form.errors.get('__all__', '')
            return JsonResponse({'error': error_message}, status=400)
    else:
        form = ImageUploadForm()
    context = {
        'form': form,
    }
    return render(request, 'img/index.html', context)


def image_list(request):
    image_items = Image.objects.all()

    
    # 페이지당 보여질 이미지 수
    items_per_page = int(request.GET.get('items_per_page', 25))  # 기본값은 25
    paginator = Paginator(image_items, items_per_page)
    
    page = request.GET.get('page')
    try:
        image_items = paginator.page(page)
    except PageNotAnInteger:
        # 페이지 파라미터가 정수가 아닌 경우, 첫 페이지를 가져옵니다.
        image_items = paginator.page(1)
    except EmptyPage:
        # 페이지가 범위를 벗어나면 마지막 페이지를 가져옵니다.
        image_items = paginator.page(paginator.num_pages)
        
    context = {
        'image_items': image_items, 
        'items_per_page': items_per_page
        }
    
    return render(request, 'img/image_list.html', context)

def search_images(request):
    query = request.GET.get('search')
    
    image_items = Image.objects.all()

    
    # 페이지당 보여질 이미지 수
    items_per_page = int(request.GET.get('items_per_page', 25))  # 기본값은 25
    paginator = Paginator(image_items, items_per_page)
    
    page = request.GET.get('page')
    try:
        image_items = paginator.page(page)
    except PageNotAnInteger:
        # 페이지 파라미터가 정수가 아닌 경우, 첫 페이지를 가져옵니다.
        image_items = paginator.page(1)
    except EmptyPage:
        # 페이지가 범위를 벗어나면 마지막 페이지를 가져옵니다.
        
        image_items = paginator.page(paginator.num_pages)
    if query:
        # 검색 내역 저장
        current_time = timezone.now()
        SearchHistory.objects.create(query=query, search_time=current_time)
        hashtag = Hashtag.objects.filter(name__icontains=query)
        search_history = (
        SearchHistory.objects
        .values('query')
        .annotate(search_count=Count('query'))
        .order_by('-search_count')[:10]
    )
    else:
        hashtag = Hashtag.objects.all()
        search_history = (
        SearchHistory.objects
        .values('query')
        .annotate(search_count=Count('query'))
        .order_by('-search_count')[:10]
    )
        
    images = Image.objects.filter(hashtags__name__icontains=query)  # 검색어를 포함하는 이미지를 필터링
    print(paginator )
    context ={
        'images': images,
        'query': query, 
        'search_history':search_history,
        'image_items': image_items, 
        'items_per_page': items_per_page
        }
    print(items_per_page)
    print(image_items)
    return render(request, 'img/search_results.html', context)

@require_POST
def download_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
  
    # 이미지 다운로드 횟수 증가
    image.download_count += 1
    image.save()

    return JsonResponse({'message': '다운로드 성공', 'download_count': image.download_count})





@csrf_exempt
def generate_ai_hashtags(request):
    if request.method == 'POST':
        print('2')
        if 'image' not in request.FILES:
            return JsonResponse({'error': '이미지가 업로드되지 않았습니다.'}, status=400)

        uploaded_file = request.FILES['image']
        image_path = default_storage.save('tmp_' + uploaded_file.name, ContentFile(uploaded_file.read()))

        try:
            print('55')
            # AI 해시태그 생성
            tags = ai_utils.generate_tags(default_storage.path(image_path))
            print(tags)
            # 영어 태그를 한국어로 번역
            print(translate_tags(tags))
            korean_tags = translate_tags(tags)
            print('korean_tags')
            return JsonResponse({'success': True, 'tags': korean_tags})
        except Exception as e:
            print('77')
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            print('88')
            # 임시 파일 삭제
            if default_storage.exists(image_path):
                default_storage.delete(image_path)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)

translator = Translator()

def translate_tags(tags):
    
    print(tags)
    """Translate a list of tags from English to Korean."""
    translations = translator.translate(tags, src='en', dest='ko')
    print(translations)
    print(translator)
    return [translation.text for translation in translations]
