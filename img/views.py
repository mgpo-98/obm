from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from img.forms import DocumentForm
import random

# Create your views here.
def index(request):
  if request.method == 'POST':
        review_form = DocumentForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            # 로그인한 유저 => 작성자네!
            review.save()
            return redirect('reviews:index')
  else: 
        review_form = DocumentForm()
  context = {
      'review_form': review_form,  
    }
  return render(request, 'img/index.html', context=context)
  


