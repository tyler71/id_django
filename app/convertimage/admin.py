from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from image_difference.models import User
from .models import ImageUnit

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

admin.site.register(User, UserAdmin)

@admin.register(ImageUnit)
class ImageUnitAdmin(admin.ModelAdmin):
    pass