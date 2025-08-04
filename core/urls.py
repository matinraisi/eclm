
from django.urls import path
from .views import *

app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('files/', FileListView.as_view(), name='file_list'),
    path('files/<int:pk>/', FileDetailView.as_view(), name='file_detail'),
]