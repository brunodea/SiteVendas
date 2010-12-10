from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
   (r'^$', 'users.views.index'),
   (r'^user/login$', login),
   (r'^user/logout$', logout),
   (r'^user/register$', 'users.views.register'),
   (r'^user/cart/$', 'users.views.userCart'),
   (r'^search/$', 'products.views.searchProduct'),
   (r'^admin/addproduct$', 'products.views.addProduct'),
   (r'^admin/editcategories$', 'products.views.editCategories'),
   (r'^products/$', 'products.views.listProducts'),
   (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),  
   (r'^admin/', include(admin.site.urls))
)
