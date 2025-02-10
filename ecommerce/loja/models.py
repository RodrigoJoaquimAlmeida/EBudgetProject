from django.db import models
from django.contrib.auth.models import User
from .nome_imagem import produto_imagem_path
from django.db import IntegrityError

# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    razaosocial = models.CharField(max_length=200, null=True, blank=True)
    cnpj = models.CharField(max_length=200, null=True, blank=True)
    protheus = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    telefone = models.CharField(max_length=200, null=True, blank=True)
    id_sessao = models.CharField(max_length=200, null=True, blank=True)
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    is_created_by_site = models.BooleanField(default=False)

    def __str__(self):
        return str(self.email)
    
    def get_first_name(self):
        return self.nome.split(" ")[0]
    
    def save(self, *args, **kwargs):
        # Somente cria o `User` se não for criado pelo site
        if not self.is_created_by_site and not self.usuario:
            # Verifique se já existe um usuário com o mesmo e-mail
            try:
                user, created = User.objects.get_or_create(
                    username=self.email,
                    defaults={'email': self.email}
                )
                if created:
                    user.set_password(self.protheus)  # senha temporária
                    user.save()
                self.usuario = user
            except IntegrityError:
                pass
        super(Cliente, self).save(*args, **kwargs)

class Categoria(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.nome)

class Grupo(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL)
    slug = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.nome)

class Medida(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.nome)

class Foto(models.Model):
    imagem = models.ImageField(upload_to=produto_imagem_path, null=True, blank=True)

    def __str__(self):
        return f"ID: {self.id} - {str(self.imagem)}"

class Produto(models.Model):
    imagem = models.ManyToManyField(Foto, blank=True, related_name='produtos')
    nome = models.CharField(max_length=200, null=True, blank=True)
    SKU = models.CharField(max_length=10, null=True, blank=True)
    fardo = models.IntegerField(default=0)
    ativo =models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL)
    grupo = models.ForeignKey(Grupo, null=True, blank=True, on_delete=models.SET_NULL)
    medida = models.ForeignKey(Medida, null=True, blank=True, on_delete=models.SET_NULL)
    texto = models.TextField(max_length=999, null=True, blank=True)

    def __str__(self):
        return f'SKU: {str(self.SKU)}, Descrição: {str(self.nome)}, Categoria: {str(self.categoria)}, Grupo: {str(self.grupo)}, Fardo/Volume: {str(self.fardo)}, Medida: {str(self.medida)}'

    def total_orcados(self):
        itens = ItensOrcamento.objects.filter(orcamento__finalizado=True, item_estoque__produto=self.id)
        total = sum([item.quantidade for item in itens])
        return total

class Cor(models.Model):
    nome = models.CharField(max_length=100, null=True, blank=True)
    codigo = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.nome)

class ItemEstoque(models.Model):
    produto = models.ForeignKey(Produto, null=True, blank=True, on_delete=models.SET_NULL)
    cor = models.ForeignKey(Cor, null=True, blank=True, on_delete=models.SET_NULL)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return f"Código: {str(self.produto.SKU)} - Descrição: {str(self.produto.nome)} - Quantidade: {str(self.quantidade)} {str(self.produto.medida)} - Cor: {str(self.cor)}"

class Endereco(models.Model):
    rua = models.CharField(max_length=200, null=True, blank=True)
    numero = models.IntegerField(default=0)
    complemento = models.CharField(max_length=200, null=True, blank=True)
    cep = models.CharField(max_length=20, null=True, blank=True)
    cidade = models.CharField(max_length=50, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'Cliente: {str(self.cliente.razaosocial)} - Endereço: {str(self.rua)}, {str(self.complemento)}, {str(self.cidade)}, {str(self.estado)}, CEP: {str(self.cep)}'

class Orcamento(models.Model):
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    finalizado = models.BooleanField(default=False)
    codigo_orcamento = models.CharField(max_length=200, null=True, blank=True)
    endereco = models.ForeignKey(Endereco, null=True, blank=True, on_delete=models.SET_NULL)
    data_finalizacao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Cliente: {self.cliente.razaosocial} - id_orcamento: {self.id} - Finalizado: {self.finalizado}"
    
    @property
    def quantidade_total(self):
        itens_orcamento = ItensOrcamento.objects.filter(orcamento__id=self.id)
        quantidade = sum([item.quantidade for item in itens_orcamento])
        return quantidade
    
    @property
    def itens(self):
        itens_orcamento = ItensOrcamento.objects.filter(orcamento__id=self.id)
        return itens_orcamento


class ItensOrcamento(models.Model):
    item_estoque = models.ForeignKey(ItemEstoque, null=True, blank=True, on_delete=models.SET_NULL)
    quantidade = models.IntegerField(default=0)
    orcamento = models.ForeignKey(Orcamento, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"id_orcamento: {self.orcamento.id} - SKU: {self.item_estoque.produto.SKU} - Descrição: {self.item_estoque.produto.nome} - Quantidade: {self.quantidade}"
    


class Banner(models.Model):
    imagem = models.ImageField(null=True, blank=True)
    link_destino = models.CharField(max_length=400, null=True, blank=True)
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return f"Banner: {str(self.link_destino)} - Ativo: {str(self.ativo)}"
    
class OrcamentosSalvos(models.Model):
    formulario = models.FileField(null=True, blank=True)
    orcamento = models.ForeignKey(Orcamento, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        formulario_path = self.formulario.path
        formulario_nome = formulario_path.split("formularios\\")[-1]
        return formulario_nome


