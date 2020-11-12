from django.db import models

class ConversionType(models.Model):
    name = models.CharField(max_length=20)

class Users(models.Model):
    name         = models.CharField(max_length=100)
    create_date  = models.DateTimeField()
    token        = models.CharField(max_length=100)

class ImageUnit(models.Model):
    result       = models.CharField(max_length=100, blank=True)
    images_used  = models.IntegerField()
    conversion   = models.ForeignKey(ConversionType, null=True, on_delete=models.SET_NULL)
    submitted    = models.DateTimeField()
    submitted_by = models.ForeignKey(Users, on_delete=models.CASCADE)
