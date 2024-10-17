from django.shortcuts import render, redirect
from .models import *
import uuid
from .utils import filtrar_produtos, ordenar_produtos, exporta_dados_orcamento
from .criarformcheckout import criar_formulario
from .enviarformcheckoutemail import enviar_email
from .apikommo import object_kommo
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime


# Create your views here.
def homepage(request):
    banners = Banner.objects.filter(ativo=True)
    context = {"banners": banners}
    return render(request, 'homepage.html', context)


def loja(request, filtro=None):
    descricao = request.GET.get('descricao', '')
    produtos = Produto.objects.filter(ativo=True)
    if descricao:
        produtos = produtos.filter(nome__icontains=descricao)
    produtos = filtrar_produtos(produtos, filtro)
    if request.method == "POST":
        dados = request.POST.dict()     
        print(dados) 
        if "grupo" in dados:
            produtos = produtos.filter(grupo__slug=dados.get("grupo"))
        if "categoria" in dados:
            produtos = produtos.filter(categoria__slug=dados.get("categoria"))
    ids_categorias = produtos.values_list("categoria", flat=True).distinct()
    categorias = Categoria.objects.filter(id__in=ids_categorias)
    ids_grupos = produtos.values_list("grupo", flat=True).distinct()
    grupos = Grupo.objects.filter(id__in=ids_grupos)
    # itens = ItemEstoque.objects.filter(produto__in=produtos)
    ordem = request.GET.get("ordem", "")
    produtos = ordenar_produtos(produtos, ordem)
    context = {"produtos": produtos, "categorias": categorias, "grupos": grupos}
    return render(request, 'loja.html', context)


def ver_produto(request, id_produto, id_cor=None): #RETORNAR AQUI PARA AJUSTAR QUANTIDADE__GTE
    tem_estoque = False
    cores = {}
    cor_selecionada = None
    if id_cor:
        cor_selecionada = Cor.objects.get(id=id_cor)
        
    produto = Produto.objects.get(id=id_produto)
    itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gte=0) 
    if len(itens_estoque) > 0:
        tem_estoque = True
        cores = {item.cor for item in itens_estoque}
        if id_cor:
            itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gte=0, cor__id = id_cor) 
    context = {'produto': produto, 'itens_estoque': itens_estoque, 'tem_estoque': tem_estoque, 'cores': cores, 'cor_selecionada': cor_selecionada}
    return render(request, 'ver_produto.html', context)

def adicionar_carrinho(request, id_produto):
    if request.method == "POST" and id_produto:
        dados = request.POST.dict()
        cor = dados.get('cor_selecionada')
        quantidade = int(dados.get('quantidade', 1))
        if not cor:
            return redirect('loja')
        resposta = redirect('carrinho')
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            if request.COOKIES.get('id_sessao'):
                id_sessao = request.COOKIES.get('id_sessao')
            else:
                id_sessao = str(uuid.uuid4())
                resposta.set_cookie(key='id_sessao', value=id_sessao, max_age=60*60*24*7)
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
                
        orcamento, criado = Orcamento.objects.get_or_create(cliente=cliente, finalizado=False)
        item_estoque = ItemEstoque.objects.get(produto__id=id_produto, cor__id=cor)
        item_orcamento, criado = ItensOrcamento.objects.get_or_create(item_estoque=item_estoque, orcamento=orcamento)
        item_orcamento.quantidade += quantidade
        item_orcamento.save()
        return resposta
    else:
        return redirect('loja')
    
def remover_carrinho(request, id_produto):
    if request.method == "POST" and id_produto:
        dados = request.POST.dict()
        cor = dados.get('cor_selecionada')
        quantidade = int(dados.get('quantidade', 1))
        if not cor:
            return redirect('ver_produto')
        
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            if request.COOKIES.get('id_sessao'):
                id_sessao = request.COOKIES.get('id_sessao')
                cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            else:
                return redirect('loja')       
        orcamento, criado = Orcamento.objects.get_or_create(cliente=cliente, finalizado=False)
        item_estoque = ItemEstoque.objects.get(produto__id=id_produto, cor__id=cor)
        item_orcamento, criado = ItensOrcamento.objects.get_or_create(item_estoque=item_estoque, orcamento=orcamento)
        item_orcamento.quantidade -= quantidade
        item_orcamento.save()
        if item_orcamento.quantidade <= 0:
            item_orcamento.delete()
        return redirect('carrinho')
    else:
        return redirect('loja')


def carrinho(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get('id_sessao'):
            id_sessao = request.COOKIES.get('id_sessao')
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            context = {'cliente_existente': False, 'itens_orcamento': None, 'orcamento': None}
            return render(request, 'carrinho.html', context)
    orcamento, criado = Orcamento.objects.get_or_create(cliente=cliente, finalizado=False)
    itens_orcamento = ItensOrcamento.objects.filter(orcamento=orcamento)
    context = {"itens_orcamento": itens_orcamento, "orcamento": orcamento, 'cliente_existente': True}
    return render(request, 'carrinho.html', context)

@login_required
def checkout(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get('id_sessao'):
            id_sessao = request.COOKIES.get('id_sessao')
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:          
            return redirect('loja')
    orcamento, criado = Orcamento.objects.get_or_create(cliente=cliente, finalizado=False)
    enderecos = Endereco.objects.filter(cliente=cliente)
    context = {"orcamento": orcamento, "enderecos": enderecos, 'erro': None}
    return render(request, 'checkout.html', context)

@login_required
def finalizar_orcamento(request, id_orcamento):
    if request.method == "POST":
        erro = None
        dados = request.POST.dict()
        total = dados.get('total')
        orcamento = Orcamento.objects.get(id=id_orcamento)

        if int(total) != int(orcamento.quantidade_total):
            erro = 'quantidade'

        if not "endereco" in dados:
            erro = 'endereco'
        else:
            id_endereco = dados.get('endereco')
            endereco = Endereco.objects.get(id=id_endereco)
            orcamento.endereco = endereco
        
        codigo_orcamento = f'{orcamento.id}{datetime.now().timestamp()}'
        orcamento.codigo_orcamento = codigo_orcamento
        orcamento.save()
        if erro:
            enderecos = Endereco.objects.filter(cliente=orcamento.cliente)
            context = {"erro": erro, 'orcamento': orcamento, 'enderecos': enderecos}
            return render(request, 'checkout.html', context)
        else:
            itens_orcamento = ItensOrcamento.objects.filter(orcamento=orcamento)
            orcamento.finalizado = True
            orcamento.data_finalizacao = datetime.now()
            orcamento.save()         
            # criar_formulario(itens_orcamento)
            enviar_email(orcamento)
            # object_kommo(criar_formulario(itens_orcamento))
            return redirect('meus_orcamentos')
    else:
        return redirect('loja')

@login_required   
def adicionar_endereco(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            if request.COOKIES.get('id_sessao'):
                id_sessao = request.COOKIES.get('id_sessao')
                cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            else:          
                return redirect('loja')

        dados = request.POST.dict()
        endereco = Endereco.objects.create(cliente=cliente, rua=dados.get('rua'), numero=int(dados.get('numero')), 
                                           complemento=dados.get('complemento'), cep=dados.get('cep'), cidade=dados.get('cidade'), estado=dados.get('estado'))
        endereco.save()
        return redirect('checkout')
    else:
        context = {}
        return render(request, 'adicionar_endereco.html', context)

@login_required
def minha_conta(request):
    erro = None
    alterado = False
    if request.method == 'POST':
        dados = request.POST.dict()
        if "senha_atual" in dados:
            senha_atual = dados.get('senha_atual')
            nova_senha = dados.get('nova_senha')
            nova_senha_confirmacao = dados.get('nova_senha_confirmacao')
            if nova_senha == nova_senha_confirmacao:
                usuario = authenticate(request, username=request.user.email, password=senha_atual)
                if usuario:
                    usuario.set_password(nova_senha)
                    usuario.save()
                    alterado = True
                else:
                    erro = 'senha_incorreta'
            else:
                erro = 'senhas_divergentes'
        elif "email" in dados:
            email = dados.get("email")
            nome = dados.get("nome")
            razaosocial = dados.get("razaosocial")
            cnpjcpf = dados.get("cnpjcpf")
            telefone = dados.get("telefone")
            if email != request.user.email:
                usuarios = User.objects.filter(email=email)
                if len(usuarios) > 0:
                    erro = 'email_existente'
            if not erro:
                cliente = request.user.cliente
                cliente.email = email
                request.user.email = email
                request.user.username = email
                cliente.nome = nome
                cliente.razaosocial = razaosocial
                cliente.cnpj = cnpjcpf
                cliente.telefone = telefone
                cliente.save()
                request.user.save()
                alterado = True
            
        else:
            erro = 'formulario_invalido'
    context = {'erro': erro, 'alterado': alterado}
    return render(request, 'usuario/minha_conta.html', context)

@login_required
def meus_orcamentos(request):
    cliente = request.user.cliente
    orcamentos = Orcamento.objects.filter(finalizado=True, cliente=cliente).order_by("-data_finalizacao")
    context = {"orcamentos": orcamentos}
    return render(request, 'usuario/meus_orcamentos.html', context)


def fazer_login(request):
    erro = False
    if request.user.is_authenticated:
        return redirect('loja')
    if request.method == "POST":
        dados = request.POST.dict()
        if "email" in dados and "senha" in dados:
            email = dados.get("email")
            senha = dados.get("senha")
            usuario = authenticate(request, username=email, password=senha)
            if usuario:
                login(request, usuario)
                return redirect('loja')
            else:
                erro = True
        else:
            erro = True
    context = {"erro": erro}
    return render(request, 'usuario/fazer_login.html', context)

def criar_conta(request):
    erro = None
    if request.user.is_authenticated:
        return redirect('loja')
    if request.method == "POST":
        dados = request.POST.dict()
        if "email" in dados and "nome" in dados and "razaosocial" in dados and "cnpjcpf" in dados and "senha" in dados and "confirmacao_senha" in dados and "telefone" in dados:
            email = dados.get("email")
            nome = dados.get("nome")
            razaosocial = dados.get("razaosocial")
            cnpjcpf = dados.get("cnpjcpf")
            senha = dados.get("senha")
            confirmacao_senha = dados.get("confirmacao_senha")
            telefone = dados.get("telefone")
            try:
                validate_email(email)
            except ValidationError:
                erro = 'email_invalido'
            if senha == confirmacao_senha:
                usuario, criado = User.objects.get_or_create(username=email, email=email)
                if not criado:
                    erro = "usuario_existente"
                else:
                    usuario.set_password(senha)
                    usuario.save()

                    usuario = authenticate(request, username=email, password=senha)
                    login(request, usuario)

                    if request.COOKIES.get('id_sessao'):
                        id_sessao = request.COOKIES.get('id_sessao')
                        cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
                    else:
                        cnpjcpf = str(cnpjcpf)
                        telefone = str(telefone)
                        cliente, criado = Cliente.objects.get_or_create(email=email, nome=nome, razaosocial=razaosocial, cnpj=cnpjcpf, telefone=telefone)
                    cliente.usuario = usuario
                    cliente.email = email
                    cliente.nome = nome
                    cliente.razaosocial = razaosocial
                    cliente.cnpj = cnpjcpf
                    cliente.telefone = telefone
                    cliente.save()
                    resposta = redirect('loja')
                    resposta.delete_cookie("id_sessao")
                    return resposta
            else:
                erro = 'senhas_diferentes'
            
        else:
            erro = "preenchimento"
    context = {'erro': erro}
    return render(request, 'usuario/criar_conta.html', context)

@login_required
def fazer_logout(request):
    logout(request)
    return redirect('loja')