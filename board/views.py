from django.shortcuts import render


def board_list(request):
    return render(request, "board/board_list.html")
