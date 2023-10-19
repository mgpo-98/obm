from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .models import Image
from .forms import ImageUploadForm

# Create your views here.

def index(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_list')
    else:
        form = ImageUploadForm()
    return render(request, 'img/index.html', {'form': form})


def image_list(request):
    image_items = Image.objects.all()
    return render(request, 'img/image_list.html', {'image_items': image_items})