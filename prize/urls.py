from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^$',views.home,name='home'),
    url('^search/',views.search_results,name='search_results'),
    url(r'^profile/(?P<username>\w+)', views.profile, name='profile'),
    url(r'^uploads/',views.post_project,name='post_project'),
    url(r'^api/projects/$', views.ProjectsList.as_view()),
     url(r'^api/profile/$', views.ProfileList.as_view()),
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)