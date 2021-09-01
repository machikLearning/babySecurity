from django.db import models
from account.models import User
from rasberrypy.models import Product

# Create your models here.

class UserToken(models.Model):
    user = models.ForeignKey(User, "userId")
    token = models.CharField(max_length=60)

