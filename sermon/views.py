from django.shortcuts import render


def sermon_list(request):
    return render(request, "sermon/sermon_list.html")
