from django.shortcuts import render

# Create your views here.

def home(request):

    context = {}

    return render(request,'ashakya_api/index.html',context)

def projects(request):

    context = {}

    return render(request,'ashakya_api/project.html',context)
