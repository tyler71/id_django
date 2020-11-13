from django.contrib import admin

from .models import ImageUnit#, SubmittedImage, Users

# class SubmittedImageAdmin(admin.StackedInline):
#     model = SubmittedImage

# @admin.register(ImageUnit)
# class ImageUnitAdmin(admin.ModelAdmin):
#     inlines = [SubmittedImageAdmin]
#
#     class Meta:
#         model = ImageUnit

# @admin.register(SubmittedImage)
# class SubmittedImageAdmin(admin.ModelAdmin):
#     pass

@admin.register(ImageUnit)
class ImageUnitAdmin(admin.ModelAdmin):
    pass