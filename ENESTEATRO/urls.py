from django.conf import settings
from django.conf.urls import include, url 
from django.urls import path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.views.generic import View
from django.views.generic.edit import FormView

from search import views as search_views
from base.api.views import *
from base.forms import RegistroForm

class RegistroView(FormView):
    template_name = "application.html"
    form_class = RegistroForm 


    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        print("form enviado")
        return super().form_valid(form)
    




urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),
    url(r'^api-auth/', include('rest_framework.urls')),

    url(r'^api/v1mal/$', APIRootView.as_view()),
    url(r'^api/v1/', include('base.api.urls')),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:

    ### url(r'', include(wagtail_urls)),
    path("", RegistroView.as_view(), name="app"),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
