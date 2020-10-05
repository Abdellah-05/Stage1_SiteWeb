var compteur = 0;
var slidesImg = ["/static/images/1.jpg", "/static/images/2.png", "/static/images/3.jpg", "/static/images/4.jpg", "/static/images/5.jpg"];

var slideShow = function(){
    document.getElementById('slideImg').setAttribute('src', slidesImg[compteur])
    if (compteur < slidesImg.length - 1){
        compteur++;
    }else{
        compteur = 0;
    }
    setTimeout("slideShow()", 2000);
}
slideShow();