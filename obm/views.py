from django.shortcuts import render
from django.shortcuts import render
from img.models import SearchHistory

def main(request):
    pass
    return render(request,'main.html')

def get_realtime_search_rank(request):
    # 최근 검색 기록을 가져옴 (가장 최근에 검색된 키워드 순으로 정렬)
    recent_searches = SearchHistory.objects.order_by('-search_time')[:5]

    # 가져온 검색 기록에서 검색어만 추출
    search_rank = [search.query for search in recent_searches]

    return JsonResponse({'rank': search_rank})
