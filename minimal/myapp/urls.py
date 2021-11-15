from django.urls import path
from .views import my_view, download, videos

urlpatterns = [
    path('', my_view, name='my-view'),
    path('download/', download, name='download'),
    path('videos/', videos, name='download')
]
