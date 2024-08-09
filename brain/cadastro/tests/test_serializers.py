from django.test import TestCase
from rest_framework.exceptions import ValidationError
from cadastro.models import Produtor, Fazenda, AreaAgricultavel
from cadastro.serializers import CadastroProdutorSerializer


class CadastroProdutorSerializerTest(TestCase):
    """Teste para CadastroProdutorSerializer"""

    def setUp(self):
        # Dados iniciais para os testes
        self.produtor_data = {
            "nome": "João da Silva",
            "cpf": "333.196.070-57",
            "fazendas": [
                {
                    "nome": "Fazenda A",
                    "cidade": "São Paulo",
                    "estado": "SP",
                    "area_total": 100,
                    "area_vegetacao": 20,
                    "areas_agricultaveis": [
                        {"cultura": "Soja", "area_agricultavel": 50},
                        {"cultura": "Café", "area_agricultavel": 20}
                    ]
                },
                {
                    "nome": "Fazenda B",
                    "cidade": "Belo Horizonte",
                    "estado": "MG",
                    "area_total": 200,
                    "area_vegetacao": 50,
                    "areas_agricultaveis": [
                        {"cultura": "Algodão", "area_agricultavel": 100}
                    ]
                }
            ]
        }

    def test_valid_creation(self):
        # Testa a criação válida de um produtor com fazendas e áreas agricultáveis
        serializer = CadastroProdutorSerializer(data=self.produtor_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.assertEqual(Produtor.objects.count(), 1)
        self.assertEqual(Fazenda.objects.count(), 2)
        self.assertEqual(AreaAgricultavel.objects.count(), 3)

        fazenda_a = Fazenda.objects.get(nome='Fazenda A')
        self.assertEqual(fazenda_a.area_total, 100)
        self.assertEqual(fazenda_a.areas_agricultaveis.count(), 2)

    def test_invalid_creation_missing_cpf_and_cnpj(self):
        # Testa a criação inválida de um produtor sem CPF e CNPJ
        self.produtor_data['cpf'] = None
        serializer = CadastroProdutorSerializer(data=self.produtor_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_creation_area_exceeds_total(self):
        # Testa a criação inválida de uma fazenda onde a soma da área agric. e vegetação excede a área total
        self.produtor_data['fazendas'][0]['areas_agricultaveis'][0]['area_agricultavel'] = 85
        serializer = CadastroProdutorSerializer(data=self.produtor_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_update_produtor(self):
        # Testa a atualização de um produtor existente
        serializer = CadastroProdutorSerializer(data=self.produtor_data)
        self.assertTrue(serializer.is_valid())
        produtor = serializer.save()

        updated_data = {
            'nome': 'João da Silva Filho',
            'cpf': '333.196.070-57',
            'fazendas': [
                {
                    'id': produtor.fazendas.first().id,
                    'nome': 'Fazenda A Atualizada',
                    "cidade": "São Paulo",
                    "estado": "SP",
                    'area_total': 150,
                    'area_vegetacao': 30,
                    'areas_agricultaveis': [
                        {'id': produtor.fazendas.first().areas_agricultaveis.first().id,
                         'cultura': "Soja", 'area_agricultavel': 70}
                    ]
                }
            ]
        }
        serializer = CadastroProdutorSerializer(produtor, data=updated_data)
        self.assertTrue(serializer.is_valid())
        updated_produtor = serializer.save()

        self.assertEqual(updated_produtor.nome, 'João da Silva Filho')
        self.assertEqual(updated_produtor.fazendas.count(), 1)
        self.assertEqual(updated_produtor.fazendas.first().nome, 'Fazenda A Atualizada')
        self.assertEqual(updated_produtor.fazendas.first().areas_agricultaveis.count(), 1)

    def test_delete_fazendas_not_in_request(self):
        # Testa a exclusão de fazendas que não estão na requisição de atualização
        serializer = CadastroProdutorSerializer(data=self.produtor_data)
        self.assertTrue(serializer.is_valid())
        produtor = serializer.save()

        updated_data = {
            "nome": "João da Silva",
            "cpf": "333.196.070-57",
            "fazendas": [
                {
                    "nome": "Fazenda A",
                    "cidade": "São Paulo",
                    "estado": "SP",
                    "area_total": 100,
                    "area_vegetacao": 20,
                    "areas_agricultaveis": [
                        {"cultura": "Soja", "area_agricultavel": 50},
                        {"cultura": "Café", "area_agricultavel": 20}
                    ]
                }
            ]
        }
        serializer = CadastroProdutorSerializer(produtor, data=updated_data)
        self.assertTrue(serializer.is_valid())
        updated_produtor = serializer.save()

        self.assertEqual(updated_produtor.fazendas.count(), 1)  # Verifica se uma fazenda foi removida
        self.assertEqual(Fazenda.objects.count(), 1)  # Verifica se a fazenda foi deletada
