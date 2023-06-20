from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from img.forms import ReviewForm
from .models import Review


# Create your views here.
def index(request):
  image = Review.objects.all()
  if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review_form.save()
            return redirect('/')
  else: 
        review_form = ReviewForm()
  context = {
      'review_form': review_form,  
      'image' : image,
    }
  return render(request, 'img/index.html', context=context)
  


