from django.urls import path, include
from cadastro.views import CadastroProdutorView, DashboardFazendasView
from rest_framework import routers, serializers, viewsets

# adiciona os cadastro_produtores
router = routers.DefaultRouter()
router.register(r'cadastro_produtores', CadastroProdutorView)
router.register(r'dashboard_fazendas', DashboardFazendasView, basename='dashboard_fazendas')


urlpatterns = [
    path('api/', include(router.urls)),
]
