from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("users/", include("users.urls", namespace="users")),
    path("intro/", include("intro.urls", namespace="intro")),
    path("awake/", include("awake.urls", namespace="awake")),
    path("sermon/", include("sermon.urls", namespace="sermon")),
    path("board/", include("board.urls", namespace="board")),
    path("gallary/", include("gallary.urls", namespace="gallary")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
