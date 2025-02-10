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