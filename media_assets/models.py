from django.db import models
from django.conf import settings
import cloudinary
from cloudinary.models import CloudinaryField

# Create your models here.
class MediaAssets(models.Model):
    
    CATEGORY_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
    )
    # object attributes / table field 
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="Uploaded and maintained by MediaHUB")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='image')
    media_file = CloudinaryField('media', resource_type='auto') # cloudinary in use
    # relationship attribute  # object relationship - 'has a' : one user can have many uploads 
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='media_assets')
    created_at =  models.DateTimeField(auto_now_add=True) # automatically capture the time when a record is inserted 
    updated_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)