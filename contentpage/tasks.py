import logging

from django.db import transaction

from content_page_test_task.celery import app
from contentpage.models import PageContent


@app.task(bind=True)
def counter_task(self, page_id):
    page_contents = PageContent.objects.select_related('content').select_for_update().filter(page=page_id)
    with transaction.atomic():
        for page_content in page_contents:
            page_content.content.counter += 1
            page_content.content.save()
