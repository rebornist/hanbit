# https://docs.djangoproject.com/ko/3.0/ref/models/fields/
from django.db import models
from . import managers


class TimeStampedModel(models.Model):
    """ Time Stamped Model """

    """ Models에 기본저으로 들어갈 항목 """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()

    class Meta:
        abstract = True  # 데이터 베이스에 등록되지 않은 추상 모델 다른 모델 확장에만 사용
