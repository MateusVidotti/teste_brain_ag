from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path



urlpatterns = [
    path('', include('cadastro.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += staticfiles_urlpatterns()
