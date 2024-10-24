from django.db import models

# Create your models here.

from common.models import BaseModel
from user.models import User

class Post(BaseModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(verbose_name="Cunteúdo do post", max_length=128)
    # image = ImageField
    # parent = ForeignKey(null=True)

