# Generated by Django 5.1.2 on 2024-10-27 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0018_fotos_remove_produto_imagem_produto_imagem'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Fotos',
            new_name='Foto',
        ),
    ]
