from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^$',views.home,name='home'),
    url('^search/',views.search_results,name='search_results'),
    url(r'^profile/(?P<username>\w+)', views.profile, name='profile'),
    url(r'^uploads/',views.post_recipe,name='post_recipe'),
    url(r'^api/recipes/$', views.RecipesList.as_view(),name='recipe_name'),
    url(r'^api/profile/$', views.ProfileList.as_view(),name='profile_name'),
    url(r'^recipe/(\d+)',views.recipe,name='recipes'),
    
]

if settings.DEBUG: 
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)