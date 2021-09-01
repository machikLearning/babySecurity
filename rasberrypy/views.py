from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from account.models import User
from .models import *
import cv2 as cv
import tensorflow
import logging
import secrets
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from parent.models import UserToken
from babysecurity import settings
import requests
logger = logging.getLogger(__name__)

def frame2_happy(point):
    if bool(point) == False :
        return False
    else :
        return True
def frame3_hp(pt):
    for ptt in pt:
        u = pt[ptt]
        if u == True:
            return "0"
    if u == False:
        return "1"

def beingReverse(filePath):
    try:
        BODY_PARTS = {"Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                      "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                      "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
                      "LEye": 15, "REar": 16, "LEar": 17, "Background": 18}
        POSE_PAIRS = [["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                      ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                      ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                      ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
                      ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"]]
        net = cv.dnn.readNetFromTensorflow("./graph_opt.pb")
        img = cv.imread(filePath, cv.IMREAD_ANYCOLOR)
        net.setInput(cv.dnn.blobFromImage(img, 1.0, (368, 368), (127.5, 127.5, 127.5), swapRB=True, crop=False))
        out = net.forward()
        out = out[:, :19, :, :]
        assert (len(BODY_PARTS) == out.shape[1])
        points = []
        for i in range(len(BODY_PARTS)):
            heatMap = out[0, i, :, :]
            _, conf, _, point = cv.minMaxLoc(heatMap)
            x = (368 * point[0]) / out.shape[3]
            y = (368 * point[1]) / out.shape[2]
            points.append((int(x), int(y)) if conf > 0.2 else None)
        for pair in POSE_PAIRS:
            partFrom = pair[0]
            partTo = pair[1]
            assert (partFrom in BODY_PARTS)
            assert (partTo in BODY_PARTS)
            ap = frame2_happy(points[0])
            bp = frame2_happy(points[14])
            cp = frame2_happy(points[15])
            dp = frame2_happy(points[16])
            ep = frame2_happy(points[17])
            hp = [ap, bp, cp, dp, ep];
        result = 0
        result = frame3_hp(hp)
        return result
    except Exception as ex:
        print(ex)

def createProduction(request):
    if request.method == "POST":
        createProductionForm = CreationProductionForm(request.POST)
        if createProductionForm.is_valid():
            jsonResponse = {}
            try:
                createProduction = createProductionForm.save(commit=False)
                jsonResponse["status"] = 1
                jsonResponse["authentication"] = createProduction.authentication
                createProduction.save()
            except Exception as ex:
                logger.debug
                jsonResponse["status"] = 1
        return JsonResponse(jsonResponse)
    else:
        return render(request, "rasberrypy/createProduction.html", {
            "createProductionForm": CreationProductionForm()
        })

def productAuth(request):
    try:
        if request.method == "POST":
            productActiveForm = ProductionActiveForm(request.POST)
            jsonObject = {}
            if productActiveForm.is_valid():
                user = User.objects.get(userId=productActiveForm.cleaned_data["userId"])
                product = Product.objects.get(id=user.productionKey)
                if product.authentication == productActiveForm.cleaned_data["authentication"]:
                    product.isActive = True
                    user.is_active = True
                    product.save()
                    user.save()
            else:
                logging.debug
            return JsonResponse(jsonObject)

        else:
            return render(request, "rasberrypy/auth.html", {
            "productActiveForm": ProductionActiveForm()
            })
    except Exception as ex:
        logger.debug

def imageUpload(request):
    if request.method == "GET":
        return render(request, "rasberrypy/uploadImage.html",{
            "babyPictureForm" : BabyPictureForm()
        })
    else:
        babyPicutreForm = BabyPictureForm(request.POST,request.FILES)
        if babyPicutreForm.is_valid():
            product = Product.objects.get(authentication=babyPicutreForm.cleaned_data["authentication"])
            babyPicture = babyPicutreForm.save(commit=False)
            babyPicture.productionKey = product
            babyPicture.save()
            babyPicture.isReverse = beingReverse(settings.MEDIA_ROOT + "/" + babyPicture.realTitle)
            babyPicture.save()
            if babyPicture.isReverse:
                user = User.objects.get(productionKey=product.id)
                userToken = UserToken.objects.get(user = user )
                 
                headers = {"Authorization" : "key=AAAARenGXtY:APA91bGHctGwh5AmR7kJ6hVr0a-boD_BJoKhlHfjkswIeEJyJ91Kdp6iv3SLReRFIuRH26hUrhhM_eM8So8MGU0OLzH4jER_h5QQ8dhRCw0VeK0hv7y_HmDIxlJjZGuZpVVMcyFvqWwu",
                           "Content-Type" : "application/json"}


                dic = {"data" : {"IsReverse" : "Reverse"},"to": userToken.token,"priority":"high"}
                requests.post("https://fcm.googleapis.com/fcm/send",data=json.dumps(dic),headers = headers)
                return JsonResponse(dic)
        return render(request, "rasberrypy/uploadImage.html", {
            "babyPictureForm": BabyPictureForm()
        })

def createBabyTemperature(request):
    if request.method == "GET":
        return render(request, "rasberrypy/createBabyTemperature.html",{
            "babySickForm" : BabySickForm()
        })
    else:
        babySickForm = BabySickForm(request.POST)
        if babySickForm.is_valid():
            product = Product.objects.get(authentication=babySickForm.cleaned_data["authentication"])
            babySick = babySickForm.save(commit=False)
            babySick.productionKey = product
            babySickForm.save()


@require_POST
@csrf_exempt
def startStream(request):
    stream = get_object_or_404(Stream, key=request.POST["name"])
    if not stream.user.is_active:
        return HttpResponseForbidden("Inactive user")

    if stream.started_at:
        return HttpResponseForbidden("Already streaming")

    stream.save()

    # Redirect to the streamer's public username
    return redirect(stream.productKey)

@require_POST
@csrf_exempt
def stop_stream(request):
    Stream.objects.filter(key=request.POST["name"]).update(createTime=None)
    return HttpResponse("OK")
