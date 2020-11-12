from django.shortcuts import render, HttpResponse

def home(request):
    return render(request, 'home.html')

def new_image(request):
    return render(request, 'new_image.html')