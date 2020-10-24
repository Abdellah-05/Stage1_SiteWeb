const text = document.querySelector('.h1');
const strText = text.textContent;
const splitText = strText.split('');

text.textContent = '';
for (let e = 0; e < splitText.length; e++){
    text.innerHTML += "<span id='span1'>" + splitText[e] + "</span>";
}

let char = 0;
let compteur = setInterval(onTick, 50);

function onTick(){
    const span = text.querySelectorAll('span')[char];
    span.classList.add('fade');
    char++
    if (char === splitText.length){
        complete();
        return;
    }
    console.log(span)
}
function complete(){
    clearInterval(compteur);
    compteur = null;
}

/*------------------------------------------------------------------- */
const text2 = document.querySelector('.services');
const strText2 = text2.textContent;
const splitText2 = strText2.split('');

text2.textContent = '';
for (let i = 0; i < splitText2.length; i++){
    text2.innerHTML += "<span id='span2'>" + splitText2[i] + "</span>";
}

let char2 = 0;
let compteur2 = setInterval(onTick2, 50);

function onTick2(){
    const span2 = text2.querySelectorAll('span')[char2];
    span2.classList.add('fade2');
    char2++
    if (char2 === splitText2.length){
        complete2();
        return;
    }
}
function complete2(){
    clearInterval(compteur2);
    compteur2 = null;
}

