let elemsMenuCabeca = document.querySelectorAll(
	'.menu__subtitulo-expansivel-cabecalhos'
);

elemsMenuCabeca.forEach(function (elemt) {
	elemt.addEventListener('click', function () {
		elemt.parentElement.classList.toggle(
			'menu__subtitulo-expansivel--aberto'
		);
	});
});

let elemFecharFiltro = document.querySelector('.menu__fechar-filtro');
let elemAbrirFiltro = document.querySelector('.produtos__cabecalho-filtrar');

elemFecharFiltro.addEventListener('click', function () {
	document.body.classList.remove('filtro-aberto');
});
elemAbrirFiltro.addEventListener('click', function () {
	document.body.classList.add('filtro-aberto');
});

let url = new URL(document.URL);
let itens = document.getElementsByClassName("item-ordenar");

for (i= 0; i < itens.length; i++){
    url.searchParams.set("ordem", itens[i].value);
    itens[i].value = url.href;
    
}