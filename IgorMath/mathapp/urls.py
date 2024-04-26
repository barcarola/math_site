from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [path('', views.index, name='index'),
               path('settings/', views.settings, name='settings'),
               path('statistics/', views.statistics, name='statistics'),
               path('session_results/', views.session_results, name='session_results'),
               path('solving/', views.solving, name='solving'),
               path('register_solution/(?P<primer_type>[^/]+)\\Z/(?P<result>[^/]+)\\Z', views.register_solution, name='register_solution'),
               ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
