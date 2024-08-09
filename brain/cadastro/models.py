from cnpj_field.models import CNPJField
from cpf_field.models import CPFField
from django.db import models


CULTURA_SOJA = 'Soja'
CULTURA_MILHO = "Milho"
CULTURA_ALGODAO = "Algodão"
CULTURA_CAFE = "Café"
CULTURA_CANA_DE_AÇUCAR = "Cana-de-açucar"
CULTURA_CHOICES = (
    (CULTURA_SOJA, 'Soja'),
    (CULTURA_MILHO, 'Milho'),
    (CULTURA_ALGODAO, 'Algodao'),
    (CULTURA_CAFE, 'Café'),
    (CULTURA_CANA_DE_AÇUCAR, 'Cana-de-açucar'),
)


class Produtor(models.Model):
    """Representa um Produtor"""
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, help_text='Nome do produtor')
    cpf = CPFField('cpf', blank=True, null=True)
    cnpj = CNPJField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Produtores'

    def __str__(self):
        return self.nome


class Fazenda(models.Model):
    """Representa uma Fazenda"""
    id = models.AutoField(primary_key=True)
    produtor = models.ForeignKey(Produtor, on_delete=models.CASCADE, related_name='fazendas')
    nome = models.CharField(max_length=50, help_text='Nome da fazenda')
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2)
    area_total = models.FloatField(help_text='Área total em hectares da fazenda')
    area_vegetacao = models.FloatField(help_text='Área de vegetação em hectares')


class AreaAgricultavel(models.Model):
    """Representa uma Área Agricultavel"""
    id = models.AutoField(primary_key=True)
    fazenda = models.ForeignKey(Fazenda, on_delete=models.CASCADE,  related_name='areas_agricultaveis')
    area_agricultavel = models.FloatField(help_text='Área agricultável em hectares')
    cultura = models.CharField(max_length=20, default=CULTURA_SOJA, choices=CULTURA_CHOICES,
                               help_text='Cultura agricultável')
