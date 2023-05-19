from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import DocumentForm
import random

# Create your views here.
def index(request):

    return render(request, "img/index.html")
