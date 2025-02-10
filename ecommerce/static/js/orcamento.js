
let eleOrcamentoMenus = document.querySelectorAll('.pedido__cabecalho');
let eleOrcamentos = document.querySelectorAll('.pedido__corpo');


eleOrcamentoMenus.forEach((menu, index) => {
    menu.addEventListener('click', function () {
        eleOrcamentos[index].classList.toggle('pedido__corpo--aberto');
    });
});
