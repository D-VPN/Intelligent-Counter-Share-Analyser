from django.http import HttpResponse,HttpResponseServerError, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.views.decorators import gzip
from .models import User, RetailerUser, BrandUser, Contracts
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RetailerRegisterForm, BrandRegisterForm, RetailStoreInformationForm, ContractForm
from .divider import divide_image_into_parts, detect_brand_in_shelf
import cv2
import numpy as np
import time
import os


def get_frame():
    list_imgs = []
    camera =cv2.VideoCapture(0) 
    end_time = time.time() + 5
    while time.time() < end_time:
        _, img = camera.read()
        list_imgs.append(img)
        imgencode=cv2.imencode('.jpg',img)[1]
        #time.sleep(1)
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
    i = 0 
    path= 'D:\param\Competitions\SPIT 2021\Code\\backend\spit_backend\static\\frames'
    for img in list_imgs:
        i += 1
        cv2.imwrite(os.path.join(path,'cctv-data-'+str(i)+'.jpg'),img)
    del(camera)

@gzip.gzip_page
def camera_on(request):
    try :
        return StreamingHttpResponse(get_frame(),content_type="multipart/x-mixed-replace;boundary=frame")
    except :
        return "error"

# Create your views here.
def index(request):
    try:
        if request.user.is_retailer:
            retailer = RetailerUser.objects.get(user=request.user)
            return render(request, 'index.html', {'retailer': retailer})
        else:
            brand = BrandUser.objects.get(user=request.user)
            contracts = Contracts.objects.filter(contract_brand=brand)
            # all_contracts = []
            # for contract in contracts:
            #     temp = []
            #     retailer = contract.brand_retailer
            #     print("Hello")
            #     print(retailer.top_price)
            return render(request, 'index.html', {'contracts' : contracts})
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

@login_required
def contract_view(request, id):
    user = User.objects.get(id=id)
    retailer = RetailerUser.objects.get(user=user)
    
    if request.method == "POST":
        form = ContractForm(request.POST)
        if form.is_valid():
            contract = Contracts()
            contract.desired_positions = form.cleaned_data.get('desired_positions')
            contract.precent_visibility = form.cleaned_data.get('precent_visibility')
            contract.contract_retailer = user
            contract.contract_brand = BrandUser.objects.get(user=request.user)
            contract.save()

            return redirect('index')
        else:
            print(form.errors)
    else:
        form = ContractForm()
    return render(request, 'contract.html', {'form': form, 'this_user' : user, 'retailer' : retailer})


class RetailerListView(ListView):
    model = User
    template_name = 'brand_contract.html'
    context_object_name = 'users'


    
def verify(request):

    #defining images
    shelf_image="https://5.imimg.com/data5/SV/FD/MY-30413995/product-display-rack-500x500.jpg"
    shelf_image_2="https://cdn.kqed.org/wp-content/uploads/sites/10/2020/03/RS42182_016_KQED_SanFranciscoMarinFoodBank_03182020_9244-qut-1020x680.jpg"
    shelf_image_3="https://a57.foxnews.com/static.foxbusiness.com/foxbusiness.com/content/uploads/2020/02/931/523/Grocery-Store-iStock.jpg?ve=1&tl=1"
    shelf_production="Production Assets/Shelf.jpg"


    #1st image
    divide_image_into_parts(image=shelf_image_2, dir_name="process-images/shelf_2/columns_2",threshold_x=50,threshold_y=100,row=False,link=True,invert=True,draw=False)
    divide_image_into_parts(image="process-images/shelf_2/columns_2/column_0.png",dir_name="process-images/shelf_2/rows_2", threshold_x=50,threshold_y=150,row=True, trim=False, img_dir=True,invert=False , link=False,draw=False)
    

    #2nd image 
    divide_image_into_parts(image=shelf_production,dir_name="process-images/shelf_production/columns_production", threshold_x=10,threshold_y=600,row=False,img_dir=True,invert=True , link=True,draw=False)
    divide_image_into_parts(image="process-images/shelf_production/columns_production/column_0.png",dir_name="process-images/shelf_production/rows_production1",threshold_x=50,threshold_y=350,row=True, trim=True, img_dir=True,invert=False , link=False,draw=False)
    divide_image_into_parts(image="process-images/shelf_production/columns_production/column_1.png",dir_name="process-images/shelf_production/rows_production2",threshold_x=50,threshold_y=350,row=True, trim=True, img_dir=True,invert=False , link=False,draw=False)
    
    detect_brand_in_shelf(shelf='D:\param\Competitions\SPIT 2021\Code\ML Models\Production Assets\Shelf.jpg',brand='D:\param\Competitions\SPIT 2021\Code\ML Models\Production Assets\\brands\Oreo.jpg',dir_name='D:\param\Competitions\SPIT 2021\Code\backend\spit_backend\static\output',file_name='final-output')
    

    return render(request,'verify.html')