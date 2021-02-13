from django.http import HttpResponse,HttpResponseServerError, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.decorators import gzip
from .models import User
from .forms import RetailerRegisterForm, BrandRegisterForm
import cv2
import numpy as np
import time
import os

# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')


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
    