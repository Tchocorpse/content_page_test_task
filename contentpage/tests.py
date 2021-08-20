import copy
import json
import logging
from unittest.mock import patch

from django.forms import model_to_dict
from rest_framework.test import APITestCase

from contentpage.models import (
    Page,
    TextBaseContent,
    AudioBaseContent,
    VideoBaseContent,
    PageContent,
    BaseContent,
)

from contentpage.tasks import counter_task


def create_pages(n):
    pages_list = []
    for i in range(n):
        page = Page(title=f"test title {i}")
        pages_list.append(page)
    pages = Page.objects.bulk_create(pages_list)
    return pages


def create_content(n, page):
    content_list = []
    page_content_list = []
    for i in range(n):
        text_content = TextBaseContent(
            title=f"text title {i}", counter=0, text=f"test text {i}"
        )
        text_content.save()
        content_list.append(text_content)

        text_content_page = PageContent(
            page=page, content_order=(i + 1) * 3 - 2, content=text_content
        )
        text_content_page.save()
        page_content_list.append(text_content_page)

        audio_content = AudioBaseContent(
            title=f"audio title {i}", counter=0, bitrate=23
        )
        audio_content.save()
        content_list.append(audio_content)

        audio_content_page = PageContent(
            page=page, content_order=(i + 1) * 3 - 1, content=audio_content
        )
        audio_content_page.save()
        page_content_list.append(audio_content_page)

        video_content = VideoBaseContent(
            title=f"video title {i}",
            counter=0,
            video_file_url=f"https://www.videofiletest.org/{i}/",
            subtitles_url=f"https://www.subtitlestest.org/{i}/",
        )
        video_content.save()
        content_list.append(video_content)

        video_content_page = PageContent(
            page=page, content_order=(i + 1) * 3, content=video_content
        )
        video_content_page.save()
        page_content_list.append(video_content_page)

    return content_list, page_content_list


class GetPagesTest(APITestCase):
    def setUp(self):
        self.url = "http://testserver/pages/"
        self.pages_num = 6
        self.pages = create_pages(self.pages_num)

    def test_correct_operation_bulk(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        raw_response = response.content.decode("utf8")

        response_prepared = json.loads(raw_response)
        self.assertEqual(response_prepared["count"], Page.objects.all().count())

        response_list = response_prepared["results"]
        for page in response_list:
            test_page = Page.objects.get(pk=page["id"])
            self.assertEqual(page["id"], test_page.id)
            self.assertEqual(page["title"], test_page.title)
            self.assertEqual(
                page["created"], test_page.created.isoformat().replace("+00:00", "Z"),
            )
            self.assertEqual(
                page["updated"], test_page.updated.isoformat().replace("+00:00", "Z"),
            )
            self.assertEqual(page["url"], f"{self.url}{test_page.id}/")

    def test_correct_operation_limit_offset(self):
        limit = 2
        offset = 2
        url_lo = f'{self.url}?limit={limit}&offset={offset}'
        response = self.client.get(url_lo)
        self.assertEqual(response.status_code, 200)

        raw_response = response.content.decode("utf8")

        response_prepared = json.loads(raw_response)
        self.assertEqual(response_prepared["count"], Page.objects.all().count())

        response_list = response_prepared["results"]
        for page in response_list:
            test_page = Page.objects.get(pk=page["id"])
            self.assertEqual(page["id"], test_page.id)
            self.assertEqual(page["title"], test_page.title)
            self.assertEqual(
                page["created"], test_page.created.isoformat().replace("+00:00", "Z"),
            )
            self.assertEqual(
                page["updated"], test_page.updated.isoformat().replace("+00:00", "Z"),
            )
            self.assertEqual(page["url"], f"{self.url}{test_page.id}/")


class GetPageDetailTest(APITestCase):
    def setUp(self):
        self.url_pattern = "http://testserver/pages/"
        self.content_number = 2
        self.pages = create_pages(self.content_number)
        self.content_list, self.page_content_list = create_content(
            self.content_number, self.pages[0]
        )

    def test_request_wrong_id(self):
        wrong_id = self.pages[0].id + 10
        url = f"{self.url_pattern}{wrong_id}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.json(), {"error": f"no such page with id {wrong_id}"},
        )

    def test_correct_operation(self):
        with patch("contentpage.tasks.counter_task.apply_async") as mock_task:
            page = self.pages[0]
            url = f"{self.url_pattern}{page.id}/"

            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

            page = self.pages[0]

            prepared_response = response.json()["page_detail"]
            self.assertEqual(prepared_response["id"], page.id)
            self.assertEqual(prepared_response["title"], page.title)
            self.assertEqual(
                prepared_response["created"],
                page.created.isoformat().replace("+00:00", "Z"),
            )
            self.assertEqual(
                prepared_response["updated"],
                page.updated.isoformat().replace("+00:00", "Z"),
            )

            prepared_page_content = prepared_response["page_content"]

            for i in range(3 * self.content_number):
                test_content = model_to_dict(self.content_list[i])
                page_content = prepared_page_content[i]
                self.assertEqual(page_content, test_content)

            contents_id = tuple([content.id for content in self.content_list])
            mock_task.assert_called_with(args=[contents_id])


class CounterTaskTest(APITestCase):
    def setUp(self):
        self.page = create_pages(1)[0]
        self.content_list, self.page_content_list = create_content(1, self.page)

    def test_correct_operation(self):
        old_content_list = copy.deepcopy(self.content_list)
        counter_task(tuple([content.id for content in self.content_list]))

        for content in old_content_list:
            new_content = BaseContent.objects.get(pk=content.id)
            self.assertEqual(content.counter + 1, new_content.counter)
