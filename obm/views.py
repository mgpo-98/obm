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
    # 주어진 날짜의 요일 (0: 월요일, 1: 화요일, ..., 6: 일요일)
    today_weekday = date.weekday()

    # 일주일 간격의 시작일 계산 (월요일 00:00:00 기준)
    start_of_week = date - timedelta(days=today_weekday, hours=date.hour, minutes=date.minute, seconds=date.second, microseconds=date.microsecond)

    return start_of_week

def get_popular_search_rank(request):
    period = request.GET.get('period', 'overall')
 # 현재 날짜 및 시간
    now = timezone.now()

    print(period)
    # period에 따라 필터링
    if period == 'daily':
        field_name = 'daily_rank'
        # 당일의 시작 시간 (00:00:00)
        start_date = datetime(now.year, now.month, now.day, 0, 0, 0)
        # 당일의 종료 시간 (23:59:59)
        end_date = datetime(now.year, now.month, now.day, 23, 59, 59)
    elif period == 'weekly':
        field_name = 'weekly_rank'
        # 주어진 날짜의 주의 시작 날짜 (월요일을 시작으로 한다고 가정)
        start_date = get_start_of_week(now)
        # 주의 시작 날짜의 종료 시간 (23:59:59)
        end_date = datetime(now.year, now.month, now.day, 23, 59, 59)
    else:
        field_name = 'overall_rank'
        # 최초 검색 이후의 날짜 및 시간 (전체 기간)
        start_date = SearchHistory.objects.aggregate(Min('search_time'))['search_time__min']
        # 현재 날짜의 종료 시간 (23:59:59)
        end_date = datetime(now.year, now.month, now.day, 23, 59, 59)

    search_history = (
        SearchHistory.objects
        .filter(search_time__range=(start_date, end_date))  # start_date와 end_date 사이의 기록만 필터링
        .values('query', field_name)
        .annotate(search_count=Count('query'))
        .order_by('-search_count')[:10])
    
    
    rank_data = [{'query': item['query'], 'rank': item[field_name], 'search_count': item['search_count']} for item in search_history]
     # 이전 검색어 순위 가져오기
    prev_search_rank = request.session.get('prev_search_rank', {})
       # 검색어 순위 변동 체크 및 저장
    for item in rank_data:
        prev_rank = prev_search_rank.get(item['query'], 0)
        item['arrow'] = get_arrow(prev_rank, item['rank'])
        item['new'] = '' if prev_rank == 0 else ''
    # 현재 검색어 순위를 이전 순위로 저장
    request.session['prev_search_rank'] = {item['query']: item['rank'] for item in rank_data}

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
