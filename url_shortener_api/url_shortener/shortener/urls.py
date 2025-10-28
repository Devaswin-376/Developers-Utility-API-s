from django.urls import path
from .views import ShortenURLView, URLListView, RedirectView, DeleteShortURLView

urlpatterns = [
    path('shorten/', ShortenURLView.as_view(), name='shorten-url'),
    path('urls/', URLListView.as_view(), name='url-list'),
    path('short/<str:short_code>/', RedirectView.as_view(), name='redirect-url'),
    path('delete/<int:id>/', DeleteShortURLView.as_view(), name='delete-url'),
]
