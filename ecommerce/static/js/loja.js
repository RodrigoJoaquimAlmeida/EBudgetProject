function redirectToPage() {
	let selectElement = document.getElementsByClassName('produtos__select')[0];
	let selectedOption = selectElement.options[selectElement.selectedIndex].value;
	if (selectedOption) {
		window.location.href = selectedOption
	}
}

let elemsMenuCabecalho = document.querySelectorAll(
	'.menu__subtitulo-expansivel-cabecalhos'
);

elemsMenuCabecalho.forEach(function (ele) {
	ele.addEventListener('click', function () {
		ele.parentElement.classList.toggle(
			'menu__subtitulo-expansivel--aberto'
		);
	});
});
