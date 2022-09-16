from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    path('ritzy/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'Ritzy Fashion Hub'
admin.site.site_title = 'Ritzy Admin Portal'
admin.site.index_title = 'Welcome to Ritzy Fashion Portal'