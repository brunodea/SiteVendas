from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings

from users.views import register

admin.autodiscover()

urlpatterns = patterns('',
   (r'^$', 'users.views.index'),
   (r'^login/', login),
   (r'^logout/', logout),
   (r'^register/', register),
   (r'^admin/addproduct/', 'products.views.addProduct'),
   (r'^listproducts/', 'products.views.listProducts'),
   (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),  
   (r'^admin/', include(admin.site.urls))
)
