let elemsCarrosselBotao = document.querySelectorAll('.carrossel__botao');
let elemCarrosselImagens = document.querySelector('.carrossel__imagens');

function rodarCarrossel(i) {
	let itemAnt = i - 1;

	if (i == 0) {
		itemAnt = elemsCarrosselBotao.length - 1;
	}

	elemsCarrosselBotao[itemAnt]
		.querySelector('div')
		.classList.remove('carrossel__preenchimento--completo');

	elemCarrosselImagens.style = 'transform: translateX(-' + i * 100 + '%)';

	elemsCarrosselBotao[i]
		.querySelector('div')
		.classList.add('carrossel__preenchimento--completo');

	let proxItem = i + 1;

	if (i == elemsCarrosselBotao.length - 1) {
		proxItem = 0;
	}

	setTimeout(function () {
		rodarCarrossel(proxItem);
	}, 5000);
}

setTimeout(function () {
	rodarCarrossel(0);
}, 1000);

let eleCabecalhoMenu = document.querySelector('.cabecalho__menu');
let eleCabecalho = document.querySelector('.cabecalho');
let elemsItemLista = document.querySelectorAll('.cabecalho__item-lista');

eleCabecalhoMenu.addEventListener('click', function () {
	eleCabecalho.classList.toggle('cabecalho--aberto');

	elemsItemLista.forEach(function (ele) {
		ele.querySelector('.cabecalho__link').href = 'javascript: void(0)';
	});
});

elemsItemLista.forEach(function (ele) {
	ele.addEventListener('click', function () {
		ele.classList.toggle('cabecalho__item-lista--aberto');
	});
});

let eleCabecalhoLogin = document.querySelector('.cabecalho__icone-login');
let eleInfosPerfil = document.querySelector('.cabecalho__informacoes-perfil');
// let eleIconePerfil = document.querySelector('.cabecalho__link-icone');

eleCabecalhoLogin.addEventListener('click', function () {
	eleInfosPerfil.classList.toggle('cabecalho__informacoes-perfil--aberto');
	// eleIconePerfil.classList.toggle('cabecalho__link-icone--logado');
});

let elemFecharFiltro = document.querySelector('.menu__fechar-filtro');
let elemAbrirFiltro = document.querySelector('.produtos__cabecalho-filtrar');

elemFecharFiltro.addEventListener('click', function () {
	document.body.classList.remove('filtro-aberto');
});
elemAbrirFiltro.addEventListener('click', function () {
	document.body.classList.add('filtro-aberto');
});
