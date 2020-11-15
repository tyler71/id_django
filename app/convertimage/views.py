from django.shortcuts import render
from datetime import datetime


from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import ImageUnit
from .forms import NewImageForm
from .utils import conversion_choices

def home(request):
    ImageUnit.objects.filter()
    if request.method == 'POST':
        context = process_image(request)
        img_hash = context['img_hash']
        if request.session.get('related_images', None) is None:
            request.session['related_images'] = list()
        request.session['related_images'].append(img_hash)
        context['request'] = request
        return render(request, 'home.html', context)
    else:
        form = NewImageForm()
    return render(request, 'home.html', {'new_image_form': form})

def process_image(request):
        form = NewImageForm(request.POST, request.FILES)
        if form.is_valid():
            submitted_images = [img for img in request.FILES.getlist('images')]
            img_count = len(submitted_images)
            selected_method = form.cleaned_data['type']
            img = conversion_choices[selected_method](submitted_images)
            converted_img = img.return_image()
            converted_img_name = img.image_hash() + '.jpg'
            data = ImageUnit()
            data.hash = img.image_hash()
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
            content = {
                'img_hash'  : img.img_hash(),
                'img_object': data,
            }
            return content
