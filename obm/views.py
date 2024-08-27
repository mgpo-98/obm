from django.shortcuts import render
from img.models import SearchHistory,Image
from django.http import JsonResponse
from django.db.models import Count
from datetime import timedelta, date
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Min
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

def get_start_of_week(date):
   
    today_weekday = date.weekday()

    # 일주일 간격의 시작일 계산 
    start_of_week = date - timedelta(days=today_weekday, hours=date.hour, minutes=date.minute, seconds=date.second, microseconds=date.microsecond)

    return start_of_week

def get_popular_search_rank(request):
    period = request.GET.get('period', 'overall')
    # 현재 날짜 및 시간
    now = timezone.now()

    new_search_period = timedelta(hours=1)

    # period에 따라 필터링
    if period == 'daily':
        field_name = 'daily_rank'
        # 당일의 시작 시간 
        start_date = datetime(now.year, now.month, now.day, 0, 0, 0)
        start_date = timezone.now() - new_search_period
        # 당일의 종료 시간 
        end_date = datetime(now.year, now.month, now.day, 23, 59, 59)
    elif period == 'weekly':
        field_name = 'weekly_rank'
        # 주어진 날짜의 주의 시작 날짜 
        start_date = get_start_of_week(now)
        # 주의 시작 날짜의 종료 시간 
        end_date = datetime(now.year, now.month, now.day, 23, 59, 59)
    else:
        field_name = 'overall_rank'
        # 최초 검색 이후의 날짜 및 시간 (전체 기간)
        start_date = SearchHistory.objects.aggregate(Min('search_time'))['search_time__min']
        # 현재 날짜의 종료
        end_date = datetime(now.year, now.month, now.day, 23, 59, 59)

    search_history = (
        SearchHistory.objects
        .filter(search_time__range=(start_date, end_date))  # start_date와 end_date 사이의 기록만 필터링
        .values('query', field_name)
        .annotate(search_count=Count('query'))
        .order_by('-search_count')[:10])

    new_search_terms = set()
    rank_data = []

    # 이전 검색어 순위 가져오기
    prev_search_rank = request.session.get('prev_search_rank', {})

    for item in search_history:
        rank = item[field_name]
        query = item['query']
        search_count = item['search_count']
        
        # 새로운 검색어인지 확인하고 new_search_terms에 추가
        if query not in prev_search_rank:
            new_search_terms.add(query)
        
        # 새로운 검색어인 경우 new 표시
        new = 'new' if query in new_search_terms else ''
        
        # 이전 순위 가져오기
        prev_rank = prev_search_rank.get(query, 0)
        
        # 변동 화살표 구하기
        arrow = get_arrow(prev_rank, rank)
        
        # 현재 검색어를 이전 순위로 저장
        prev_search_rank[query] = rank
        
        # 랭크 데이터에 추가
        rank_data.append({
            'query': query,
            'rank': rank,
            'search_count': item['search_count'],
            'new': 'new' if query not in prev_search_rank else '',
            'arrow': arrow,
            'prev_rank': prev_rank  # 이전 랭크 추가
        })
    
    # 현재 검색어 순위를 세션에 저장
    request.session['prev_search_rank'] = prev_search_rank

    return JsonResponse({'rank': rank_data, 'period': period})


def main(request):
    
    popular_images = Image.objects.exclude(download_count=0).order_by('-download_count')[:6] 

    context = {'popular_images': popular_images}
    return render(request, 'main.html', context)




@csrf_exempt    
@require_POST
def download_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
  
    # 이미지 다운로드 횟수 증가
    image.download_count += 1
    image.save()

    return JsonResponse({'message': '다운로드 성공', 'download_count': image.download_count})

def get_arrow(prev_rank, current_rank):
    if prev_rank == current_rank:
        return ''  # 변동 없음
    elif prev_rank < current_rank:
        return '↑'  # 상승 화살표
    else:
        return '↓'  # 하락 화살표
