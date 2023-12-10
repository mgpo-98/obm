from django.shortcuts import render
from img.models import SearchHistory
from django.http import JsonResponse
from django.db.models import Count
def main(request):
    pass
    return render(request,'main.html')

def get_realtime_search_rank(request):
    # 최근 검색 기록을 가져옴 (가장 최근에 검색된 키워드 순으로 정렬)
    search_history = (
        SearchHistory.objects
        .values('query')
        .annotate(search_count=Count('query'))
        .order_by('-search_count')[:10])
 
    # 가져온 검색 기록에서 검색어만 추출
    rank_data = [{'query': item['query'], 'search_count': item['search_count']} for item in search_history]
    
    return JsonResponse({'rank_data': rank_data})

