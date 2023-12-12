from django.shortcuts import render
from img.models import SearchHistory
from django.http import JsonResponse
from django.db.models import Count

def get_popular_search_rank(request, period='daily'):
    # period에 따라 필터링
    if period == 'daily':
        field_name = 'daily_rank'
    elif period == 'weekly':
        field_name = 'weekly_rank'
    else:
        field_name = 'overall_rank'

    search_history = (
        SearchHistory.objects
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
        item['new'] = 'NEW' if prev_rank == 0 else ''

    # 현재 검색어 순위를 이전 순위로 저장
    request.session['prev_search_rank'] = {item['query']: item['rank'] for item in rank_data}

    return JsonResponse({'rank': rank_data, 'period': period})

def main(request):
    return render(request, 'main.html')

def get_arrow(prev_rank, current_rank):
    if prev_rank < current_rank:
        return '↑';  # 상승 화살표
    elif prev_rank > current_rank:
        return '↓';  # 하락 화살표
    else:
        return '';  # 변동 없음
    