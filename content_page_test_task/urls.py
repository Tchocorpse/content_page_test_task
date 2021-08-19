from django.contrib import admin
from django.urls import path

from contentpage.views import GetPages, GetPageDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', GetPages.as_view()),
    path('pages/<int:pk>/', GetPageDetail.as_view()),
]
