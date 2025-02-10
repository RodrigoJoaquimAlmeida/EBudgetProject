from django.core.mail import EmailMessage
from datetime import datetime
import pytz

def enviar_email(orcamento, camend):
    email = orcamento.cliente.email
    assunto = 'Metalforte WebServices - Orçamento Nº {} - {}'.format(orcamento.id, datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M:%S'))                                                                                                                                                                                                                                                                                                                
    corpo = f"""Prezado {orcamento.cliente.razaosocial}, Data Orçamento: {(orcamento.data_finalizacao).strftime('%d/%m/%Y %H:%M:%S')}\n
Seu Orçamento Nº {str(orcamento.id).zfill(6)} com um total de {orcamento.quantidade_total} Produtos se encontra em anexo.\n
A Metalforte agradece o seu interesse e informamos que nossos vendedores receberão uma cópia deste orçamento.\n
Caso deseje conversar com o nosso WhatsApp, entre neste link: https://wa.me/62992386584?text=Teste ou pelo telefone (62) 3219-4999.\n
\nAtenciosamente,\n\nMetalforte Web Services - Metalforte Indústria Metalúrgica Ltda
Rodovia BR-153 Km 08 Quadra 70-A, Vila Brasília
Aparecida de Goiânia - GO - CEP: 74911-410
(62) 3219 4999\nO Melhor do Aço para Você !"""        
    remetente = "Metalforte Web Services"
    prepemail = EmailMessage(assunto, corpo, remetente, [email, "rodrigo.joaquim@metalforte.com.br"])
    formula = camend

    prepemail.attach_file(formula)

    prepemail.send()