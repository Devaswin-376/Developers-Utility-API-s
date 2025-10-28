from django.urls import path
from .views import IPLookupView, MyIPView, IPListView, IPDeleteView

urlpatterns = [
    path('lookup/', IPLookupView.as_view(), name='ip-lookup'),
    path('myip/', MyIPView.as_view(), name='my-ip'),
    path('list/', IPListView.as_view(), name='ip-list'),
    path('delete/<int:id>/', IPDeleteView.as_view(), name='ip-delete'),
]
