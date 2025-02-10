import requests
from .models import Orcamento
from django.conf import settings

def send_to_kommo(orcamento_id):
    try:
        orcamento = Orcamento.objects.get(id=orcamento_id)
    except Orcamento.DoesNotExist:
        return {"error": "Orçamento não encontrado"}
  
    url = f"{settings.KOMMO_API_BASE_URL}/api/v4/lead"  # pegar url Kommo
    headers = {
        "Authorization": f"Bearer {settings.KOMMO_LONG_LIVED_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "codigo_orcamento": orcamento.codigo_orcamento,
        "data_finalizacao": orcamento.data_finalizacao.isoformat() if orcamento.data_finalizacao else None,
        "cliente": {
            "nome": orcamento.cliente.nome,
            "email": orcamento.cliente.email,
            "telefone": orcamento.cliente.telefone,
        },
        "endereco": {
            "rua": orcamento.endereco.rua,
            "numero": orcamento.endereco.numero,
            "complemento": orcamento.endereco.complemento,
            "cidade": orcamento.endereco.cidade,
            "estado": orcamento.endereco.estado,
        },
        "data_finalizacao": orcamento.data_finalizacao.isoformat() if orcamento.data_finalizacao else None,
        "finalizado": orcamento.finalizado,
        "quantidade_total": orcamento.quantidade_total, 
        "itens_orcamento": [
            {
                "item_estoque_id": item.item_estoque.id if item.item_estoque else None,
                "produto_nome": item.item_estoque.produto.nome if item.item_estoque else "N/A",
                "cor": item.item_estoque.cor.nome if item.item_estoque and item.item_estoque.cor else "N/A",
                "quantidade": item.quantidade
            }
            for item in orcamento.itens  # Lista de itens individuais com detalhes
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  
        print("Dados enviados com sucesso ao Kommo CRM.")
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP ao enviar dados ao Kommo CRM: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Erro ao tentar enviar dados ao Kommo CRM: {err}")
    else:
        if response.status_code == 200:
            print("Dados enviados com sucesso ao Kommo CRM.")
        else:
            print("Falha ao enviar dados ao Kommo CRM:", response.json())