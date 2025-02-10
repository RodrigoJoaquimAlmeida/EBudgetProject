from .models import Orcamento, ItensOrcamento, Cliente, Categoria, Grupo, Banner


def carrinho(request):
    quantidade_produtos_carrinho = 0
    if request.user.is_authenticated: 
        cliente = request.user.cliente
    else:
        if request.COOKIES.get('id_sessao'):
            id_sessao = request.COOKIES.get('id_sessao')
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            return {"quantidade_produtos_carrinho": quantidade_produtos_carrinho}
    orcamento, criado = Orcamento.objects.get_or_create(cliente=cliente, finalizado=False)
    itens_orcamento = ItensOrcamento.objects.filter(orcamento=orcamento)
    for item in itens_orcamento:
        quantidade_produtos_carrinho += item.quantidade
    return {"quantidade_produtos_carrinho": quantidade_produtos_carrinho}


def categorias_grupos(request):
    categorias_nav = Categoria.objects.all()
    grupos_nav = Grupo.objects.all()
    banners_nav = Banner.objects.all()
    return {'grupos_nav': grupos_nav, 'categorias_nav': categorias_nav, 'banners_nav': banners_nav}

