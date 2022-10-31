from django.urls import include , path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# print(urlpatterns)
print(settings.STATIC_URL , settings.STATIC_ROOT )
#/static/ None

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# [<URLResolver <URLPattern list> (admin:admin) 'admin/'>, <URLResolver 
# <module 'chat.urls' from 'P:\\my VideoChat-Django-main\\.\\chat\\urls.py'> (None:None) ''>,
#  <URLPattern '^static/(?P<path>.*)$'>]