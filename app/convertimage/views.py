from django.shortcuts import render
from datetime import datetime


from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import ImageUnit
from .forms import NewImageForm
from .utils import conversion_choices

def home(request):
    if request.method == 'POST':
        return render(request, 'home.html', new_image(request))
    else:
        form = NewImageForm()
    return render(request, 'home.html', {'new_image_form': form})

def new_image(request):
        form = NewImageForm(request.POST, request.FILES)
        if form.is_valid():
            submitted_images = [img for img in request.FILES.getlist('images')]
            img_count = len(submitted_images)
            selected_method = form.cleaned_data['type']
            converted_img = conversion_choices[selected_method](submitted_images).return_image()
            converted_img_name = 'image'
            data = ImageUnit()
            data.images_used = img_count
            data.conversion = selected_method
            data.submitted = datetime.now()
            data.result.save(converted_img_name, InMemoryUploadedFile(
                converted_img,
                None,
                converted_img_name,
                'image/jpeg',
                converted_img.tell(),
                None,
            ))
            data.save()
            return {'img_object': data}
