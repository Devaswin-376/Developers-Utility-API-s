from django.urls import path
from .views import FileUploadView, FileListView, FileDetailView, FileDeleteView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('files/', FileListView.as_view(), name='file-list'),
    path('files/<int:id>/', FileDetailView.as_view(), name='file-detail'),
    path('files/delete/<int:id>/', FileDeleteView.as_view(), name='file-delete'),
]
