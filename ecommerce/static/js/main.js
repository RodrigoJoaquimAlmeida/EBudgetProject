let url = new URL(document.URL);
let itens = document.getElementsByClassName("item-ordenar");

for (i= 0; i < itens.length; i++){
    url.searchParams.set("ordem", itens[i].value);
    itens[i].value = url.href;
    
}

