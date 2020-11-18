from django.db import models


class ImageUnit(models.Model):
    result       = models.ImageField(upload_to='imgs')
    images_used  = models.IntegerField()
    conversion   = models.CharField(max_length=20)
    submitted    = models.DateTimeField(auto_now_add=True)
    img_hash     = models.CharField(max_length=50)
    # submitted_by = models.ForeignKey(Users, on_delete=models.CASCADE)

