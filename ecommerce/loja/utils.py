

def filtrar_produtos(produtos, filtro):
    if filtro:
        if "-" in filtro:
            categoria, grupo = filtro.split("-")
            produtos = produtos.filter(grupo__slug=grupo, categoria__slug=categoria)
        else:
            produtos = produtos.filter(categoria__slug=filtro)
    return produtos

def ordenar_produtos(produtos, ordem):
    if ordem == "mais-orcados":
        lista_produtos = []
        for produto in produtos:
            lista_produtos.append((produto.total_orcados(), produto))
        lista_produtos = sorted(lista_produtos, reverse=True, key=lambda tupla: tupla[0])
        produtos = [item[1] for item in lista_produtos]
            
    return produtos

def exporta_dados_orcamento(itens_orcamento):
    lista_export_orcamento = []
    lista_export_cliente = []
    lista_export_endereco = []
    for item in itens_orcamento:
        id_orcamento = item.orcamento.id
        total_orcamento = item.item_estoque.produto.total
        sku = item.item_estoque.produto.SKU
        descricao_produto = item.item_estoque.produto.nome
        quantidade_solicitado = item.quantidade
        medida_produto = item.item_estoque.produto.medida.nome
        cor_produto = item.item_estoque.cor.nome
        codigo_website = item.orcamento.codigo_orcamento

        id_protheus = item.orcamento.cliente.protheus
        id_cliente = item.orcamento.cliente.id
        nome = item.orcamento.cliente.nome
        razaosocial = item.orcamento.cliente.razaosocial
        cnpjcpf = item.orcamento.cliente.cnpj
        email = item.orcamento.cliente.email
        telefone = item.orcamento.cliente.telefone

        id_endereco = item.orcamento.endereco.id
        ruaavenida = item.orcamento.endereco.rua
        numero_endereco = item.orcamento.endereco.numero
        complemento = item.orcamento.endereco.complemento
        cidade = item.orcamento.endereco.cidade
        estado = item.orcamento.endereco.estado
        cep = item.orcamento.endereco.cep

        lista_export_orcamento.append({"id_orcamento": id_orcamento, "total_orcamento": total_orcamento, "sku": sku, "descricao_produto": descricao_produto,
                                       "quantidade_solicitado": quantidade_solicitado, "medida_produto": medida_produto, "cor_produto": cor_produto, "codigo_website": codigo_website})
        
        lista_export_cliente.append({"id_protheus": id_protheus, "id_cliente": id_cliente, "nome": nome, "razaosocial": razaosocial, "cnpjcpf": cnpjcpf, "email": email, 
                                     "telefone":telefone})
        
        lista_export_endereco.append({"id_endereco": id_endereco, "ruaavenida": ruaavenida, "numero_endereco": numero_endereco, "complemento": complemento, "cidade": cidade, 
                                      "estado": estado, "cep": cep})
    
    return [lista_export_orcamento, lista_export_cliente, lista_export_endereco]

