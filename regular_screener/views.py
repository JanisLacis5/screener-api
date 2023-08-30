from django.shortcuts import render
from django.http import HttpResponse

def say_hi(req):
    return HttpResponse('hello')