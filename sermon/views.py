from django.shortcuts import render
from django.views.generic import DetailView

from . import models


def sermon_list(request):
    return render(request, "sermon/sermon_list.html")


class SermonDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Sermon
