from django.shortcuts import render
from img.models import SearchHistory
from django.http import JsonResponse
from django.db.models import Count

def get_realtime_search_rank(request):
    search_history = (
        SearchHistory.objects
        .values('query')
        .annotate(search_count=Count('query'))
        .order_by('-search_count')[:10])
  
    rank_data = [{'query': item['query'], 'search_count': item['search_count']} for item in search_history]
   
    return JsonResponse({'rank': rank_data})

def main(request):
    query = request.GET.get('search')
    search_history = (
        SearchHistory.objects
        .annotate(search_count=Count('query'))
        .order_by('-search_count')[:10])

    
    return render(request, 'main.html', {'search_history': search_history})