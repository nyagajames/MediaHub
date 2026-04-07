

from django.contrib import admin
'''include allows us to register paths from
an independent app'''
from django.urls import path,include
'''configure paths for images/media access i.e. those not uploaded
to cloudinary'''
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]

## set up special url path for loading assets i.e. images uploaded 
## that are not on cloudinary
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=
    settings.MEDIA_ROOT)