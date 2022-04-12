// Скрипт для формы загрузки изображений

const inputLogo = document.getElementById('logo-icon');
const previewLogo = document.getElementById('logo-icon-preview');
inputLogo.addEventListener('change', function () {
    if (this.files &&
        this.files.length) {
        previewLogo.src = window.URL.createObjectURL(this.files[0]);
        previewLogo.setAttribute('height', '100%');
    } else {
        previewLogo.setAttribute('height', '100%');
        previewLogo.src = "../assets/empty-club-icon.png";
    }
});

const inputCoach = document.getElementById('coach-icon');
const previewCoach = document.getElementById('coach-icon-preview');
inputCoach.addEventListener('change', function () {
    if (this.files &&
        this.files.length) {
        previewCoach.src = window.URL.createObjectURL(this.files[0]);
        previewCoach.setAttribute('height', '100%');
    } else {
        previewCoach.setAttribute('height', '100%');
        previewCoach.src = "../assets/empty-coach-icon.png";
    }
});

const inputPoster = document.getElementById('event-poster');
const previewPoster = document.getElementById('event-poster-preview');
inputPoster.addEventListener('change', function() {
    if (this.files &&
        this.files.length) {
        previewPoster.src = window.URL.createObjectURL(this.files[0]);
        previewPoster.setAttribute('height', '100%');
    } else {
        previewPoster.setAttribute('height', '100px');
        previewPoster.src = "../assets/empty-poster.png";
    }
});

