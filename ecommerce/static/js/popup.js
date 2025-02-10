let elemFecharPopup = document.querySelector('.popup__fechar')
let elemFecharPopupDiv = document.querySelector('.popup')

elemFecharPopup.addEventListener('click', function(){
	elemFecharPopupDiv.classList.add('popup--fechar')
})