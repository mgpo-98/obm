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