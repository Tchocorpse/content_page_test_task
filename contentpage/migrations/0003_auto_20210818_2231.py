# Generated by Django 3.2.6 on 2021-08-18 22:31

from django.db import migrations
from django.contrib.contenttypes.models import ContentType


def database_test_data_filler(apps, schema_editor):
    Page = apps.get_model('contentpage', 'Page')
    PageContent = apps.get_model('contentpage', 'PageContent')

    VideoBaseContent = apps.get_model('contentpage', 'VideoBaseContent')
    AudioBaseContent = apps.get_model('contentpage', 'AudioBaseContent')
    TextBaseContent = apps.get_model('contentpage', 'TextBaseContent')

    def create_page(title):
        new_page = Page(title=title)
        new_page.save()
        return new_page

    def create_text_content(title):
        new_text_content = TextBaseContent(title=title, counter=0, text='place holder')
        new_text_content.save()
        return new_text_content

    def create_audio_content(title):
        new_audio_content = AudioBaseContent(title=title, counter=0, bitrate=23)
        new_audio_content.save()
        return new_audio_content

    def create_video_content(title):
        new_video_content = VideoBaseContent(
            title=title,
            counter=0,
            video_file_url='https://www.videofiletest.org/',
            subtitles_url='https://www.subtitlestest.org/'
        )
        new_video_content.save()
        return new_video_content

    def assign_content_to_page(page, content, order):
        new_page_content = PageContent(page=page, content=content, content_order=order)
        new_page_content.save()

    empty_page = create_page('empty page')

    text_content_1 = create_text_content('text content 1')
    audio_content_1 = create_audio_content('audio content 1')
    video_content_1 = create_video_content('video content 1')

    single_content_page = create_page('single content page')
    assign_content_to_page(single_content_page, text_content_1, 1)

    two_content_page = create_page('two content page')
    assign_content_to_page(two_content_page, audio_content_1, 1)
    assign_content_to_page(two_content_page, video_content_1, 2)

    page_with_all_used_content_1 = create_page('used content page')
    assign_content_to_page(page_with_all_used_content_1, text_content_1, 1)
    assign_content_to_page(page_with_all_used_content_1, audio_content_1, 2)
    assign_content_to_page(page_with_all_used_content_1, video_content_1, 3)

    text_content_2 = create_text_content('text content 2')
    text_content_3 = create_text_content('text content 3')
    text_content_4 = create_text_content('text content 4')
    audio_content_2 = create_audio_content('audio content 2')
    video_content_2 = create_video_content('video content 2')
    video_content_3 = create_video_content('video content 3')

    multi_content_page = create_page('multi content page')
    multicontent_list = [
        text_content_2,
        video_content_2,
        audio_content_2,
        video_content_3,
        text_content_3,
        text_content_4,
    ]
    order = 1
    for content in multicontent_list:
        assign_content_to_page(multi_content_page, content, order)
        order += 1

    new_text_ct = ContentType.objects.get_for_model(TextBaseContent)
    TextBaseContent.objects.filter(polymorphic_ctype__isnull=True).update(polymorphic_ctype=new_text_ct)

    new_audio_ct = ContentType.objects.get_for_model(AudioBaseContent)
    AudioBaseContent.objects.filter(polymorphic_ctype__isnull=True).update(polymorphic_ctype=new_audio_ct)

    new_video_ct = ContentType.objects.get_for_model(VideoBaseContent)
    VideoBaseContent.objects.filter(polymorphic_ctype__isnull=True).update(polymorphic_ctype=new_video_ct)


class Migration(migrations.Migration):

    dependencies = [
        ('contentpage', '0002_page_title'),
    ]

    operations = [
        migrations.RunPython(database_test_data_filler),
    ]
