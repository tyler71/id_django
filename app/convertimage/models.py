from django.db import models

class Users(models.Model):
    name         = models.CharField(max_length=100)
    create_date  = models.DateTimeField()
    token        = models.CharField(max_length=100)

class ImageUnit(models.Model):
    result       = models.ImageField
    images_used  = models.IntegerField()
    conversion   = models.CharField(max_length=20)
    submitted    = models.DateTimeField()
    submitted_by = models.ForeignKey(Users, on_delete=models.CASCADE)

class SubmittedImage(models.Model):
    imageunit    = models.ForeignKey(ImageUnit, on_delete=models.CASCADE)
    image        = models.FileField(upload_to='pending_conversion')

