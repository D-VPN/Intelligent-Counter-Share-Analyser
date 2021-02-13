from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login
from .models import User, RetailerUser, BrandUser
from django.contrib.auth.decorators import login_required
from .forms import RetailerRegisterForm, BrandRegisterForm, RetailStoreInformationForm

# Create your views here.
def index(request):
    try:
        retailer = RetailerUser.objects.get(user=request.user)
        return render(request, 'index.html', {'retailer': retailer})
    except:
        return render(request, 'index.html')
    
def register(request):
    return render(request,'register.html')
    
class RetailerRegisterView(CreateView):
    model = User
    form_class = RetailerRegisterForm
    template_name = 'register-retailer.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'retailer'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('login')


class BrandRegisterView(CreateView):
    model = User
    form_class = BrandRegisterForm
    template_name = 'register-brand.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'brand'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('login')
    
@login_required
def retailer_info(request):
    if request.method == 'POST':
        form = RetailStoreInformationForm(request.POST)
        if form.is_valid():
            # form.save()
            retailer = RetailerUser.objects.get(user=request.user)
            print(form.cleaned_data.get('premium_positions'))
            retailer.no_of_aisles = form.cleaned_data.get('no_of_aisles')
            retailer.premium_positions = form.cleaned_data.get('premium_positions')
            retailer.top_price = form.cleaned_data.get('top_price')
            retailer.bottom_price = form.cleaned_data.get('bottom_price')
            retailer.middle_price = form.cleaned_data.get('middle_price')
            retailer.corner_price = form.cleaned_data.get('corner_price')
            retailer.save()
            return redirect('index')

        else:
            print(form.errors)
    else:
        form = RetailStoreInformationForm()
    return render(request, 'retailer_info.html', {'form': form})
            