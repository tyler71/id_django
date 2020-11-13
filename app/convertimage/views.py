from django.shortcuts import render, HttpResponse

from .forms import NewImageForm
from .utils import ImageMean, ImageMode, ImageMedian

def home(request):
    return render(request, 'home.html')

def new_image(request):
    if request.method == 'POST':
        form = NewImageForm(request.POST, request.FILES)
        if form.is_valid():
            submitted_images = [img for img in request.FILES.getlist('images')]

    else:
        form = NewImageForm()
    return render(request, 'new_image.html', {'new_image_form': form})
