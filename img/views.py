from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import DocumentForm
import random
# Create your views here.
def index(request):

    return render(request, 'img/index.html')

class DocumentCreateView(FormView):
    template_name = "img/index.html"
    form_class = DocumentForm
    success_url = reverse_lazy('document_list')

    def form_valid(self, form):
        if self.request.FILES:
            form.instance.attached = self.request.FILES['zzal']
        form.save()
        return super().form_valid(form)
    
def create(request, item_id):
    item_title = request.GET.get('item_title')
    print(request.GET.get('item_title'))
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            # 로그인한 유저 => 작성자네!
            review.user = request.user 
            review.item_id = item_id
            review.item_title = item_title
            review.save()
            messages.success(request, '리뷰 작성이 완료되었습니다.')
            return redirect('reviews:index')
    else: 
        review_form = ReviewForm()
    context = {
        'review_form': review_form,
        'item_title': request.GET.get('item_title')
    }
    return render(request, 'img/form.html', context=context)


def make_ladder(insert): #!ladder a b c d/1 1 2 2
    #a b c d/1 1 2 2
    key = (insert.split('/'))[0]
    now_key = key.split()
    value = (insert.split('/'))[1]
    now_value = value.split()
    if len(now_key) != len(now_value): #길이가 맞지 않을때 !! (짝이 맞지 않는 경우)
        return False,False
    else:
        random.shuffle(now_value)
        return now_key,now_value