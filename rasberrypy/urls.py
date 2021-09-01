from django.conf.urls import url
from . import views



def fakeView(*args, **kwargs):
    raise Exception("This should never be called!")


urlpatterns=[
    url(r'productAuth',views.productAuth,name="productionAuth"),
    url(r'createProduction',views.createProduction, name="createProduction"),
    url(r'imageUpload',views.imageUpload,name="imageUpload"),
    url(r'createBabyTemperature',views.createBabyTemperature, name="createBabyTemperature"),
    url(r"startStream", views.startStream, name="startStream"),
    url(r"stopStream", views.startStream, name="stopStream"),
    url("live/<productionKey>/index.m3u8", fakeView, name="hlsUrl")
]