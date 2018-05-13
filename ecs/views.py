from django.shortcuts import render
from hwcloudapi import EcsInfo
from django.http import HttpResponse

def ecsList(request):

    ecslist_dict = EcsInfo.EcsClass().getEcsDataByDjango()

    return render(request, 'ecsList.html', ecslist_dict)

def getEcsData(request):
    return HttpResponse('')

# Create your views here.
