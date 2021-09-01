from django.shortcuts import render

# Create your views here.

def badRequestPage(request):
    return render(request, "errorpage/errorBad.html",{})

def pageNotFoundPage(requset):
    return render(requset,"errorpage/errorNotFound.html",{})

def serverErrorPage(request):
    return render(request,"errorpage/errorServerError.html",{})