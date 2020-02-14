from django.shortcuts import render


def awake(request):
    return render(request, "awake/awake.html")
