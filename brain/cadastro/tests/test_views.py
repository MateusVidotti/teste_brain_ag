from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from cadastro.models import AreaAgricultavel, Fazenda, Produtor


class DashboardFazendasViewTest(TestCase):
    """Teste para DashboardFazendasView"""

    def setUp(self):
        # Cria dados iniciais para o teste
        self.client = APIClient()
        # Cria fazendas e áreas agricultáveis para o teste
        produtor1 = Produtor.objects.create(nome='Robson Cruz', cpf='333.196.070-57')
        fazenda1 = Fazenda.objects.create(produtor=produtor1, nome='Fazenda A', area_total=200, area_vegetacao=20, estado='SP')
        fazenda2 = Fazenda.objects.create(produtor=produtor1, nome='Fazenda B', area_total=300, area_vegetacao=50, estado='MG')
        AreaAgricultavel.objects.create(fazenda=fazenda1, cultura='Soja', area_agricultavel=50)
        AreaAgricultavel.objects.create(fazenda=fazenda1, cultura='Café', area_agricultavel=20)
        AreaAgricultavel.objects.create(fazenda=fazenda2, cultura='Algodão', area_agricultavel=100)

    def test_dashboard_fazendas_view(self):
        # Faz uma requisição GET para a view de dashboard
        url = reverse('dashboard_fazendas')
        response = self.client.get(url)  # Altere a URL para a rota correta

        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        # Verifica os dados retornados
        self.assertEqual(data['total_fazendas'], 2)
        self.assertEqual(data['total_hectares'], 500.0)
        self.assertEqual(data['grafico_pizza_estado']['SP'], 200.0)
        self.assertEqual(data['grafico_pizza_estado']['MG'], 300.0)
        self.assertEqual(data['grafico_pizza_cultura']['Soja'], 50.0)
        self.assertEqual(data['grafico_pizza_cultura']['Café'], 20.0)
        self.assertEqual(data['grafico_pizza_cultura']['Algodão'], 100.0)
        self.assertEqual(data['grafico_pizza_uso_solo']['Área Agricultável'], 170.0)
        self.assertEqual(data['grafico_pizza_uso_solo']['Área Vegetação'], 70.0)

