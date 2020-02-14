from django.shortcuts import render


def intro(request):
    return render(request, "intro/intro.html")
