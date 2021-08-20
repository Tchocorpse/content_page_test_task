import logging

from django.db import transaction

from content_page_test_task.celery import app
from contentpage.models import BaseContent


@app.task(bind=True)
def counter_task(self, contents_id):
    page_contents = BaseContent.objects.select_for_update().filter(id__in=contents_id)
    with transaction.atomic():
        for page_content in page_contents:
            page_content.counter += 1
        BaseContent.objects.bulk_update(page_contents, ['counter'])
