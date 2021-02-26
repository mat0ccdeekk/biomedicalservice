from django.shortcuts import render, HttpResponseRedirect

def homepage(request):
    return HttpResponseRedirect('/admin/')
