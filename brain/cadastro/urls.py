from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cadastro.views import CadastroProdutorView, DashboardFazendasView

router = DefaultRouter()
router.register(r'api/cadastro_produtores', CadastroProdutorView)

urlpatterns = [
    path('', include(router.urls)),
    path('api/dashboard_fazendas', DashboardFazendasView.as_view(), name='dashboard_fazendas')
]

