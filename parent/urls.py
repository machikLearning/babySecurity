from django.conf.urls import url
from . import views


urlpatterns=[
    url(r'main',views.main,name='main'),
    url(r'productionConfigure', views.setConfigure,name="productionConfigure"),
url(r'createToken', views.createToken, name="createToken")
]
