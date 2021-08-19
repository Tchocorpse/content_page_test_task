from django.db import models
from polymorphic.models import PolymorphicModel


class Page(models.Model):
    id = models.AutoField(primary_key=True)

    title = models.CharField(verbose_name="Заголовок", max_length=255, blank=False, null=False)

    created = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    updated = models.DateTimeField(auto_now=True, blank=False, null=False)

    def __str__(self):
        return self.title


class BaseContent(PolymorphicModel):
    id = models.AutoField(primary_key=True)

    title = models.CharField(verbose_name="Заголовок", max_length=255, blank=False, null=False)
    counter = models.IntegerField(verbose_name="Счетчик просмотров", blank=False, null=False)

    def __str__(self):
        return self.title


class VideoBaseContent(BaseContent):
    video_file_url = models.URLField(verbose_name="ссылка на видеофайл", max_length=255, blank=False, null=False)
    subtitles_url = models.URLField(verbose_name="ссылка на субтитры", max_length=255, blank=False, null=False)


class AudioBaseContent(BaseContent):
    bitrate = models.IntegerField(verbose_name="битрейт", blank=False, null=False)


class TextBaseContent(BaseContent):
    text = models.TextField(verbose_name="Текст", blank=False, null=False)


class PageContent(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    content = models.ForeignKey(BaseContent, on_delete=models.CASCADE)

    content_order = models.IntegerField(verbose_name="порядок", blank=False, null=False)
