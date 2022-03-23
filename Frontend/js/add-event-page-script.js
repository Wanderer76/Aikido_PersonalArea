//ВЫДЕЛИТЬ ЗДЕСЬ ФУНКЦИЮ
function updateImageLogo() {
    if (this.files &&
        this.files.length) {
        previewLogo.src = window.URL.createObjectURL(this.files[0]);
        previewLogo.setAttribute('height', '100%');
    } else {
        previewLogo.setAttribute('height', '100px');
        previewLogo.src = "../assets/empty-club-icon.png";
    }
}
const inputLogo = document.getElementById('logo-icon');
const previewLogo = document.getElementById('logo-icon-preview');
inputLogo.addEventListener('change', updateImageLogo);

//ВЫДЕЛИТЬ ЗДЕСЬ ФУНКЦИЮ
function updateImageCoach() {
    if (this.files &&
        this.files.length) {
        previewCoach.src = window.URL.createObjectURL(this.files[0]);
        previewCoach.setAttribute('height', '100%');
    } else {
        previewCoach.setAttribute('height', '100px');
        previewCoach.src = "../assets/empty-coach-icon.png";
    }
}
//ВЫДЕЛИТЬ ЗДЕСЬ ФУНКЦИЮ
const inputCoach = document.getElementById('coach-icon');
const previewCoach = document.getElementById('coach-icon-preview');
inputCoach.addEventListener('change', updateImageCoach);


function updateImagePoster() {
    if (this.files &&
        this.files.length) {
        previewPoster.src = window.URL.createObjectURL(this.files[0]);
        previewPoster.setAttribute('height', '100%');
    } else {
        previewPoster.setAttribute('height', '100px');
        previewPoster.src = "../assets/empty-poster.png";
    }
}

//const inputPoster = document.getElementById('event-poster');
//const previewPoster = document.getElementById('event-poster-preview');
//inputPoster.addEventListener('change', updateImagePoster);

//Переделать на Яндекс Карты
// Initialize and add the map

function initMap() {
    var map = new ymaps.Map("map", {
        center: [56.838048312714704,60.60364972721357],
        zoom: 15
    });
}

ymaps.ready(initMap);

