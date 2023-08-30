from django.shortcuts import render
from django.http import HttpResponse

def say_hi(data):
    string = f'say_hi function called, i = {0}'
    print(string)
    return HttpResponse(string)