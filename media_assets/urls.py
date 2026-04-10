from django.urls import path
'''import the views from the media_assets app'''
from . import views
## give a label for the routes : 'media_assets:home'
app_name = 'media_assets'
## register the urls paths by mapping to appropriate
## view method 
urlpatterns = [
    # '' : root path : 8000/ : this is the default path when we access the app
    path('', views.dashboard_view, name='dashboard'),
    path('my_media/', views.my_media_view, name='my_media'),
    path('upload/', views.upload_view, name='upload_view'),
    path('media/<int:pk>/', views.media_detail_view, name='media_detail'),
    path('media/<int:pk>/edit/', views.edit_media_view, name='edit_media'),
    path('media/<int:pk>/delete/', views.delete_media_view, name='delete_media'),
]