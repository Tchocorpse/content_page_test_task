import logging

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView

from contentpage.models import Page, BaseContent, PageContent
from contentpage.tasks import counter_task


class GetPages(APIView):
    def get(self, request):
        url_pattern = f'{request.build_absolute_uri("/")}pages/'
        pages_raw = Page.objects.all()

        paginator = LimitOffsetPagination()
        pages = paginator.paginate_queryset(pages_raw, request)

        result = []
        for page in pages:
            page_dict = {
                'id': page.id,
                'title': page.title,
                'created': page.created,
                'updated': page.updated,
                'url': f'{url_pattern}{page.id}/'
            }
            result.append(page_dict)

        return paginator.get_paginated_response(result)


class GetPageDetail(APIView):
    def get(self, request, pk):
        try:
            page = Page.objects.get(pk=pk)
        except Page.DoesNotExist:
            return JsonResponse({'error': f'no such page with id {pk}'}, status=400)

        contents_id = PageContent.objects.filter(page=page).order_by('content_order').values_list('content', flat=True)

        raw_contents = BaseContent.objects.filter(id__in=contents_id)

        content_list = []
        for c_id in contents_id:
            content = raw_contents.get(pk=c_id)
            content_dict = model_to_dict(content)
            content_list.append(content_dict)

        result = {
            'page_id': page.id,
            'page_title': page.title,
            'created': page.created,
            'updated': page.updated,
            'page_content': content_list,
        }
        counter_task.apply_async(args=[pk])

        return JsonResponse({'page_detail': result}, status=200)
