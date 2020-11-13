from django.shortcuts import render, HttpResponse, redirect

from .forms import NewImageForm
from .utils import ImageMean, ImageMode, ImageMedian

conversion_types = {
    "Mean": ImageMean,
    "Median": ImageMedian,
    "Mode": ImageMode,
}

def home(request, data=None):
    return render(request, 'home.html')

def new_image(request):
    if request.method == 'POST':
        form = NewImageForm(request.POST, request.FILES)
        if form.is_valid():
            submitted_images = [img for img in request.FILES.getlist('images')]
            img_count = len(submitted_images)
            selected_method = form.cleaned_data['type'].name
            converted_img = conversion_types[selected_method](submitted_images)
            d = {'converted_img': converted_img, 'img_count': img_count}
            return render(request, 'new_image.html', d)
    else:
        form = NewImageForm()
    return render(request, 'new_image.html', {'new_image_form': form})
