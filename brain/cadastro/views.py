from cadastro.models import AreaAgricultavel, Fazenda, Produtor
from cadastro.serializers import CadastroProdutorSerializer, DashboardFazendasSerializer
from django.db.models import FloatField, Sum
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class CadastroProdutorView(viewsets.ModelViewSet):
    """Cadastros de produtores"""
    queryset = Produtor.objects.all()
    serializer_class = CadastroProdutorSerializer


class DashboardFazendasView(viewsets.ReadOnlyModelViewSet):
    """Dashboard das fazendas"""
    permission_classes = [AllowAny]
    serializer_class = DashboardFazendasSerializer

    def list(self, request, *args, **kwargs):
        # Calcula o total de fazendas e a soma das áreas
        total_fazendas_quantidade = Fazenda.objects.count()
        total_fazendas_hectares = Fazenda.objects.aggregate(
            total_area=Sum('area_total', output_field=FloatField()))['total_area'] or 0.0
        # Gráfico de pizza por estado
        grafico_pizza_estado = Fazenda.objects.values('estado').annotate(
            total_area=Sum('area_total', output_field=FloatField()))
        # Converte o queryset para um dicionário
        grafico_pizza_estado = {item['estado']: item['total_area'] for item in grafico_pizza_estado}

        # Gráfico de pizza por cultura
        grafico_pizza_cultura = AreaAgricultavel.objects.values('cultura').annotate(
            total_area=Sum('area_agricultavel', output_field=FloatField()))
        # Converte o queryset para um dicionário
        grafico_pizza_cultura = {item['cultura']: item['total_area'] for item in grafico_pizza_cultura}

        # Gráfico de pizza por uso do solo (área agricultável e vegetação)
        total_area_vegetacao = Fazenda.objects.aggregate(
            area_vegetacao=Sum('area_vegetacao', output_field=FloatField()))['area_vegetacao'] or 0.0
        total_area_agricultavel = AreaAgricultavel.objects.aggregate(
            area_agricultavel=Sum('area_agricultavel', output_field=FloatField()))['area_agricultavel'] or 0.0

        data = {
            "total_fazendas": total_fazendas_quantidade,
            "total_hectares": total_fazendas_hectares,
            "grafico_pizza_estado": grafico_pizza_estado,
            "grafico_pizza_cultura": grafico_pizza_cultura,
            "grafico_pizza_uso_solo": {
                "Área Agricultável": total_area_agricultavel,
                "Área Vegetação": total_area_vegetacao
            }
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
