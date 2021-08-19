from django.contrib import admin

from contentpage.models import Page, VideoBaseContent, AudioBaseContent, TextBaseContent, PageContent


class PageContentInline(admin.TabularInline):
    model = PageContent


class PageAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    inlines = [PageContentInline]
    model = Page


class SearchBaseContentAdmin(admin.ModelAdmin):
    search_fields = ('title',)


class TextContentAdmin(SearchBaseContentAdmin):
    model = TextBaseContent


class AudioContentAdmin(SearchBaseContentAdmin):
    model = AudioBaseContent


class VideoContentAdmin(SearchBaseContentAdmin):
    model = VideoBaseContent


admin.site.register(Page, PageAdmin)
admin.site.register(VideoBaseContent, VideoContentAdmin)
admin.site.register(AudioBaseContent, AudioContentAdmin)
admin.site.register(TextBaseContent, TextContentAdmin)
admin.site.register(PageContent)
