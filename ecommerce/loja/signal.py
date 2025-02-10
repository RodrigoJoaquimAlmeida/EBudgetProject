from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Orcamento
from .kommo_integration import send_to_kommo  # Função que envia dados ao Kommo

@receiver(post_save, sender=Orcamento)
def orcamento_finalizado(sender, instance, created, **kwargs):
    # Verifica se o orçamento foi finalizado
    if instance.finalizado and not created:
        # Chama a função para enviar os dados ao Kommo
        response = send_to_kommo(instance.id)
        print(response)