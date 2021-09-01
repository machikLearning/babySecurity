from django.shortcuts import render, redirect
from rasberrypy.models import *
from django.contrib.auth.decorators import login_required
from .forms import *
# Create your views here.
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse

# Create your views here.

def createToken(request):
    if request.method == "GET":
        return render(request,'parent/createToken.html',{
            'createToken' : CreateToken(),
        })
    else:
        createToken = CreateToken(request.POST)
        try:
            prev = CreateToken.objects.get(userId=request.session["userId"])
            prev.token = createToken.cleaned_data["token"]
            prev.save()
        except:
            current = CreateUserForm.save(commit=False)
            current.save()
        return JsonResponse({"result" : 1})

def main(request):
    if request.session["userId"]:
        user = User.objects.get(userId=request.session["userId"])
        picture = BabyPicture.objects.filter(productionKey = user.productionKey,).order_by("-createTime",)
        if len(picture):
            picture = picture[0]
        babyStatus = BabySick.objects.filter(productionKey = user.productionKey).order_by("-createTime",)
        if len(babyStatus) :
            babyStatus = babyStatus[0]
        return render(request,"parent/main.html",{
            "picture" : picture,
            'babyStatus': babyStatus,
        })
    else:
        return redirect("/account/login")

def setConfigure(request):
    user = User.objects.get(userId=request.session["userId"])
    if request.method == "POST":
        product = ProductionConfigure(request.POST)
        product = product.save(commit=False)
        product.id = user.productionKey
        product.save()
        return redirect("main")
    else:
        product = Product.objects.get(id=user.productionKey)
        productionConfigure = ProductionConfigure()
        productionConfigure.timeConfigure = product.timeConfigure
        productionConfigure.mode = product.mode
        return render(request,"parent/productionConfigure.html",
                      {"productionConfigure" : productionConfigure})

