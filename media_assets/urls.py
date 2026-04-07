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
]