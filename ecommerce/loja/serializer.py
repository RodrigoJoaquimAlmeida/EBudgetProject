from rest_framework import serializers
from .models import Cliente, Produto, ItemEstoque, Categoria, Grupo, Medida, Cor, Foto

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nome', 'razaosocial', 'cnpj', 'protheus', 'email', 'telefone', 'id_sessao', 'usuario']


class ProdutoSerializer(serializers.ModelSerializer):
    categoria = serializers.SlugRelatedField(queryset=Categoria.objects.all(), slug_field='nome', required=False)
    grupo = serializers.SlugRelatedField(queryset=Grupo.objects.all(), slug_field='nome', required=False)
    medida = serializers.SlugRelatedField(queryset=Medida.objects.all(), slug_field='nome', required=False)
    imagem = serializers.PrimaryKeyRelatedField(many=True, queryset=Foto.objects.all(), required=False)

    class Meta:
        model = Produto
        fields = ['nome', 'SKU', 'fardo', 'ativo', 'categoria', 'grupo', 'medida', 'texto', 'imagem']

    def validate(self, data):
        categoria_nome = data.get('categoria')
        grupo_nome = data.get('grupo')
        medida_nome = data.get('medida')

        if categoria_nome and not Categoria.objects.filter(nome=categoria_nome).exists():
            raise serializers.ValidationError(f"Categoria '{categoria_nome}' não encontrada.")

        if grupo_nome and not Grupo.objects.filter(nome=grupo_nome).exists():
            raise serializers.ValidationError(f"Grupo '{grupo_nome}' não encontrado.")

        if medida_nome and not Medida.objects.filter(nome=medida_nome).exists():
            raise serializers.ValidationError(f"Medida '{medida_nome}' não encontrada.")

        print('Dados validados: ', data)
        return data

    # def create(self, validated_data):
    #     imagens = validated_data.pop('imagem', [])
    #     produto = Produto.objects.create(**validated_data)
    #     produto.imagem.set(imagens)  # Associa as imagens ao produto
    #     return produto

    # def update(self, instance, validated_data):
    #     imagens = validated_data.pop('imagem', None)
        
    #     if imagens is not None:
    #         instance.imagem.set(imagens)  # Atualiza as imagens associadas

    #     # Atualiza os demais campos
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance


class ItemEstoqueSerializer(serializers.ModelSerializer):
    produto = serializers.SlugRelatedField(queryset=Produto.objects.all(), slug_field='SKU')
    cor = serializers.CharField(source='cor.nome', required=False)

    class Meta:
        model = ItemEstoque
        fields = ['produto', 'cor', 'quantidade']

    def validate(self, data):
        if 'cor' in data:
            cor_nome = data['cor']['nome']
            cor_obj = Cor.objects.filter(nome=cor_nome).first()
            if not cor_obj:
                raise serializers.ValidationError(f"cor '{cor_nome}' não encontrada.")
            data['cor'] = cor_obj
        return data

    def validate_quantidade(self, value):
        if value < 0:
            raise serializers.ValidationError("A quantidade deve ser maior ou igual que zero.")
        return value
        

        