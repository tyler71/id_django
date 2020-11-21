import logging
from django.shortcuts import render
from django.views import View
from datetime import datetime


from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import ImageUnit
from .forms import NewImageForm
from .utils import conversion_choices

log = logging.getLogger(__name__)

class HomePage(View):
    def setup(self, request, *args, **kwargs):
        if request.session.get('related_images', None) is None:
            request.session['related_images'] = list()
        super(HomePage, self).setup(request, *args, **kwargs)

    def get(self, request):
        session_rel_img = request.session['related_images']
        log.info(session_rel_img)
        log.info(f"INFO: views/home | Session has {len(session_rel_img)} files")
        related_images = self._related_ordered_images(session_rel_img)
        context = {
            'related_images': related_images,
            'new_image_form': NewImageForm(),
        }
        return render(request, 'home.html', context)
    def post(self, request):
        data = self._process_images(request.POST, request.FILES)
        request.session['related_images'].append(data.pk)
        request.session.modified = True
        related_images = self._related_ordered_images(request.session['related_images'])
        context = {
            'related_images': related_images,
            'new_image_form': NewImageForm(),
        }
        return render(request, 'home.html', context)

    @staticmethod
    def _related_ordered_images(session_images):
        related_images = ImageUnit.objects.filter(pk__in=session_images)
        if len(related_images) > len(session_images):
            log.error(f"ERROR: views/_related_ordered_images | We shouldn't be able to get {len(related_images)} images! Only {len(session_images)} or less should be returned")
        ordered = related_images.order_by('-submitted')[:10]
        return ordered

    @staticmethod
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
