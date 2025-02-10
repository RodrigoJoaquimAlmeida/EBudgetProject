from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, ProdutoViewSet, ItemEstoqueViewSet
from . import views



router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'itens_estoque', ItemEstoqueViewSet)

urlpatterns = [
    path('', homepage, name='homepage'),
    path('loja/', loja, name='loja'),
    path('loja/<str:filtro>/', loja, name='loja'),
    path('produto/<int:id_produto>/', ver_produto, name='ver_produto'),
    path('produto/<int:id_produto>/<int:id_cor>/', ver_produto, name='ver_produto'), 
    path('carrinho/', carrinho, name='carrinho'),
    path('checkout/', checkout, name='checkout'),
    path('adicionarcarrinho/<int:id_produto>/', adicionar_carrinho, name='adicionar_carrinho'),
    path('removercarrinho/<int:id_produto>/', remover_carrinho, name='remover_carrinho'),
    path('adicionarendereco/', adicionar_endereco, name='adicionar_endereco'),
    path('finalizarorcamento/<int:id_orcamento>/', finalizar_orcamento, name='finalizar_orcamento'),
    path('minhaconta/', minha_conta, name='minha_conta'),
    path('meusorcamentos/', meus_orcamentos, name='meus_orcamentos'),
    path('exportarformulario/<int:id_orcamento>/', exportar_formulario, name='exportar_formulario'),
    path('fazerlogin/', fazer_login, name='fazer_login'),
    path('criarconta/', criar_conta, name='criar_conta'),
    path('fazerlogout/', fazer_logout, name='fazer_logout'),
    path("password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('', include(router.urls)),
    path("auth/kommo/callback/", views.kommo_callback, name="kommo_callback"),

]
