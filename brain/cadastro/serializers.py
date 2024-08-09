from django.db.models import Sum, Count
from rest_framework import serializers
from cadastro.models import Produtor, Fazenda, AreaAgricultavel


class AreaAgricultavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaAgricultavel
        fields = ['id', 'cultura', 'area_agricultavel']

    def to_internal_value(self, data):
        # Inclui o ID na validação
        ret = super().to_internal_value(data)
        ret['id'] = data.get('id', None)
        return ret


class FazendaSerializer(serializers.ModelSerializer):
    areas_agricultaveis = AreaAgricultavelSerializer(many=True)

    class Meta:
        model = Fazenda
        fields = ['id', 'nome', 'cidade', 'estado', 'area_total', 'area_vegetacao', 'areas_agricultaveis']
        extra_kwargs = {
            'id': {'required': False},
            'nome': {'required': True},
            'cidade': {'required': False},
            'estado': {'required': False},
            'area_total': {'required': True},
            'area_vegetacao': {'required': True},
            'areas_agricultaveis': {'required': False}
        }

    def to_internal_value(self, data):
        # Inclui o ID na validação
        ret = super().to_internal_value(data)
        ret['id'] = data.get('id', None)  # Captura o ID da fazenda se estiver presente
        return ret

    def validate(self, data):
        area_total = data.get('area_total', 0)
        area_vegetacao = data.get('area_vegetacao', 0)
        areas_agricultaveis_data = data.get('areas_agricultaveis', [])

        # Calcula a soma das áreas agricultáveis
        soma_area_agricultavel = sum([area_data.get('area_agricultavel', 0) for area_data in areas_agricultaveis_data])

        # Verifica se a soma da área agricultável e de vegetação excede a área total da fazenda
        if (soma_area_agricultavel + area_vegetacao) > area_total:
            raise serializers.ValidationError("A soma da área agricultável e de vegetação não pode exceder a área total"
                                              " da fazenda.")

        return data


class CadastroProdutorSerializer(serializers.ModelSerializer):
    fazendas = FazendaSerializer(many=True)

    class Meta:
        model = Produtor
        fields = ['id', 'nome', 'cpf', 'cnpj', 'fazendas']
        extra_kwargs = {
            'id': {'required': False},
            'nome': {'required': True},
            'cpf': {'required': False},
            'cnpj': {'required': False},
            'fazendas': {'required': False}
        }

    def validate(self, data):
        cpf = data.get('cpf')
        cnpj = data.get('cnpj')

        if not cpf and not cnpj:
            raise serializers.ValidationError("É necessário fornecer ao menos um dos campos: CPF ou CNPJ.")

        return data

    def create(self, validated_data):
        fazendas_data = validated_data.pop('fazendas')
        produtor = Produtor.objects.create(**validated_data)
        for fazenda_data in fazendas_data:
            areas_agricultaveis_data = fazenda_data.pop('areas_agricultaveis', [])
            fazenda = Fazenda.objects.create(produtor=produtor, **fazenda_data)
            for area_data in areas_agricultaveis_data:
                AreaAgricultavel.objects.create(fazenda=fazenda, **area_data)
        return produtor

    def update(self, instance, validated_data):
        # Atualiza o produtor
        instance.nome = validated_data.get('nome', instance.nome)
        instance.cpf = validated_data.get('cpf', instance.cpf)
        instance.cnpj = validated_data.get('cnpj', instance.cnpj)
        instance.save()

        # Atualiza ou cria fazendas
        fazendas_data = validated_data.pop('fazendas', [])
        fazenda_ids = [fazenda_data.get('id') for fazenda_data in fazendas_data if fazenda_data.get('id')]

        # Apaga fazendas que não estão na query
        for fazenda in instance.fazendas.all():
            if fazenda.id not in fazenda_ids:
                fazenda.delete()
        for fazenda_data in fazendas_data:
            fazenda_id = fazenda_data.get('id')
            fazenda, _ = Fazenda.objects.update_or_create(
                id=fazenda_id,
                defaults={
                    'produtor': instance,
                    'nome': fazenda_data.get('nome'),
                    'cidade': fazenda_data.get('cidade'),
                    'estado': fazenda_data.get('estado'),
                    'area_total': fazenda_data.get('area_total'),
                    'area_vegetacao': fazenda_data.get('area_vegetacao')
                }
            )

            # Atualiza ou cria áreas agricultáveis
            areas_agricultaveis_data = fazenda_data.pop('areas_agricultaveis', [])
            areas_ids = [area_data.get('id') for area_data in areas_agricultaveis_data if area_data.get('id')]

            # Apaga áreas agricultáveis que não estão na query
            for area in fazenda.areas_agricultaveis.all():
                if area.id not in areas_ids:
                    area.delete()
            # Cria/atualiza áreas
            for area_data in areas_agricultaveis_data:
                area_id = area_data.get('id')
                AreaAgricultavel.objects.update_or_create(
                    id=area_id,
                    defaults={
                        'fazenda': fazenda,
                        'cultura': area_data.get('cultura'),
                        'area_agricultavel': area_data.get('area_agricultavel')
                    }
                )

        return instance


class DashboardFazendasSerializer(serializers.Serializer):
    total_fazendas = serializers.IntegerField()
    total_hectares = serializers.FloatField()
    grafico_pizza_estado = serializers.DictField(child=serializers.FloatField())
    grafico_pizza_cultura = serializers.DictField(child=serializers.FloatField())
    grafico_pizza_uso_solo = serializers.DictField(child=serializers.FloatField())

