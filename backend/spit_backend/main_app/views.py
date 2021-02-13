from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .models import User
from .forms import RetailerRegisterForm, BrandRegisterForm

# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')
    
class RetailerRegisterView(CreateView):
    model = User
    form_class = RetailerRegisterForm
    template_name = 'register-retailer.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'retailer'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        form.save()
        return redirect('login')


class BrandRegisterView(CreateView):
    model = User
    form_class = BrandRegisterForm
    template_name = 'register-brand.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'brand'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        form.save()
        return redirect('login')
    