from django.db import models
import secrets
import hashlib
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse_lazy


def renamingImage(instance,filename):
    instance.fakeTitle = filename
    ext = filename.split(".")[-1]
    rawName = secrets.token_hex(16)
    strongerName = hashlib.sha256()
    strongerName.update(rawName.encode())
    strongerName = strongerName.hexdigest()
    instance.realTitle = strongerName+"."+ext
    return strongerName + "." + ext

class Product(models.Model):
    authentication = models.CharField(max_length=50,unique=True,null=False)
    createTime = models.DateTimeField(auto_now=True)
    timeConfigure = models.IntegerField(default=30,null=False)
    mode = models.BooleanField(default=False)
    isActive = models.BooleanField(default=False)



class BabyPicture(models.Model):
    productionKey = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=renamingImage, null=True)
    realTitle = models.CharField(max_length=200,null=True,unique=True)
    fakeTitle = models.CharField(max_length=200, null=True)
    createTime = models.DateTimeField(auto_now=True)
    isReverse = models.BooleanField(null=False,default=False)

    def get_absolute_url(self):
        url = reverse_lazy('detail', kwargs={'fakename': self.fakeTitle})
        return url

class BabySick(models.Model):
    productionKey = models.ForeignKey(Product,on_delete=models.CASCADE)
    IsSick = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now=True)

class Stream(models.Model):
    productKey = models.ForeignKey(Product,on_delete=models.CASCADE)
    key = models.CharField(max_length=50)
    createTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.productKey

    @property
    def is_live(self):
        return self.createTime is not None

    @property
    def hls_url(self):
        return reverse('hls_url',args=self.productKey)

@receiver(post_save, sender=Product, dispatch_uid="createStreamForProduct")
def createStreamForProduct(sender, instance=None, created=False, **kwargs):
    if created:
        Stream.object.create(productKey=instance)

