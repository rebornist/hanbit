from django.shortcuts import render


def gallary_list(request):
    return render(request, "gallary/gallary_list.html")
