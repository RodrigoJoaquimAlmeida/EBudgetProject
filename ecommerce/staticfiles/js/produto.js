let elemsProdCarrosselBotao = document.querySelectorAll(
	'.s-produto__carrossel-botao'
);
let elemProdCarrosselImagens = document.querySelector(
	'.s-produto__carrossel-itens'
);

elemsProdCarrosselBotao.forEach(function (elem, i) {
	elem.addEventListener('click', function () {
		elemProdCarrosselImagens.style =
			'transform: translateX(-' + i * 100 + '%)';
		elemsProdCarrosselBotao.forEach(function (ele) {
			if (ele != elem) {
				ele.classList.remove('s-produto__carrossel-botao--selecionado');
			} else {
				ele.classList.add('s-produto__carrossel-botao--selecionado');
			}
		});
	});
});
