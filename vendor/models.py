from django.db import models
from accounts.models import Profile

from base.models import BaseModel

# Create your models here.
class VerifyImage(BaseModel):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="product_images"
    )
    front = models.ImageField(upload_to="media/verify_vendor", blank=True, null=True)
    back = models.ImageField(upload_to="media/verify_vendor", blank=True, null=True)
