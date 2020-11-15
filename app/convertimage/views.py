from django.shortcuts import render
from datetime import datetime


from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import ImageUnit
from .forms import NewImageForm
from .utils import conversion_choices

def home(request):
    ImageUnit.objects.filter()
    if request.method == 'POST':
        data = _process_images(request.POST, request.FILES)
        data.save()
        if request.session.get('related_images', None) is None:
            request.session['related_images'] = list()
        request.session['related_images'].append(data.img_hash)
        session_rel_img = request.session['related_images']
        related_images = _related_ordered_images(session_rel_img)
        context = {
            'related_images': related_images,
            'new_image_form': NewImageForm(),
        }
        return render(request, 'home.html', context)
    else:
        form = NewImageForm()

        if request.session.get('related_images', None) is None:
            related_images = None
        else:
            session_rel_img = request.session['related_images']
            related_images = _related_ordered_images(session_rel_img)
        return render(request, 'home.html', {'related_images': related_images, 'new_image_form': form})

def _related_ordered_images(session_images):
    related_images = ImageUnit.objects.filter(img_hash__in=session_images)
    ordered = related_images.order_by('-submitted')[:10]
    return ordered

def _process_images(post, files):
    form = NewImageForm(post, files)
    if form.is_valid():
        submitted_images = [img for img in files.getlist('images')]
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
        return data