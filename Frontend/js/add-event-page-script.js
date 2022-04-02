// Скрипт для формы загрузки

const inputLogo = document.getElementById('logo-icon');
const previewLogo = document.getElementById('logo-icon-preview');
inputLogo.addEventListener('change', function () {
    if (this.files &&
        this.files.length) {
        previewLogo.src = window.URL.createObjectURL(this.files[0]);
        previewLogo.setAttribute('height', '100%');
    } else {
        previewLogo.setAttribute('height', '100px');
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
        previewCoach.setAttribute('height', '100px');
        previewCoach.src = "../assets/empty-coach-icon.png";
    }
});

//const inputPoster = document.getElementById('event-poster');
//const previewPoster = document.getElementById('event-poster-preview');
//inputPoster.addEventListener('change', function() {
//     if (this.files &&
//         this.files.length) {
//         previewPoster.src = window.URL.createObjectURL(this.files[0]);
//         previewPoster.setAttribute('height', '100%');
//     } else {
//         previewPoster.setAttribute('height', '100px');
//         previewPoster.src = "../assets/empty-poster.png";
//     }
// });

// Яндекс Карты
let coordinates = null;

function initMap() {
    var myMap = new ymaps.Map('map', {
        center: [56.838048312714704,60.60364972721357],
        zoom: 16,
        controls: []
    });

    var searchControl = new ymaps.control.SearchControl({
        options: {
            provider: 'yandex#map',
            noPlacemark: true
        }
    });

    searchControl.events.add('resultselect', function(e) {
        var index = e.get('index');
        searchControl.getResult(index).then(function(res) {

            coordinates = res.geometry.getCoordinates();
            myMap.geoObjects.removeAll();

            let placemark = new ymaps.Placemark(coordinates, {}, {});
            myMap.geoObjects.add(placemark);
        });
    })

    myMap.controls.add(searchControl);

    let eventLocation = document.getElementById('event-location');
    eventLocation.addEventListener('change', function() {
        update();
    })

    function update() {
        if (eventLocation.value) {
            searchControl.search(eventLocation.value);
        } else {
            myMap.geoObjects.removeAll();
            myMap.setCenter([56.838048312714704,60.60364972721357]);
            coordinates = null;
        }
    }
}

ymaps.ready(initMap);

//Отправка формы

const url = "http://127.0.0.1:8000/api/v1/events/create/";
let xhr = new XMLHttpRequest();
xhr.responseType = 'json';
let storage = window.sessionStorage;
let token = storage.getItem('user_token');

let createButton = document.getElementById('create');

let eventTitle = document.getElementById('event-name');
let dateStart = document.getElementById('date-start');
let dateEnd = document.getElementById('date-end');
let locationField = document.getElementById('event-location');
let respClub = document.getElementById('resp-club-select');
let leadCoach = document.getElementById('lead-coach');
let maxRang = document.getElementById('max-rang-select');

let couchImage = document.getElementById('coach-icon');
let couchXOffset = document.getElementById('coach-x-offset');
let couchYOffset = document.getElementById('coach-y-offset');

let logoImage = document.getElementById('logo-icon');
let logoXOffset = document.getElementById('logo-x-offset');
let logoYOffset = document.getElementById('logo-y-offset');

let orgName = document.getElementById('org-name');
let orgPhone = document.getElementById('org-phone');
let orgEmail = document.getElementById('org-email');


let locationMap = {
    center: [56.838048312714704,60.60364972721357],
    zoom: 15
}

let couchImg = {
    image: couchImage.value,
    x_offset: couchXOffset.value,
    y_offset: couchYOffset.value
}

let logoImg = {
    image: logoImage.value,
    x_offset: logoXOffset.value,
    y_offset: logoYOffset.value
}

let contacts = {
    org_name: orgName.value,
    org_phone: orgPhone.value,
    org_email: orgEmail.value
};

console.log("Enter")

xhr.onreadystatechange = function () {
    let data = xhr.response;
    console.log(data);
    location.href = '../html/admin-page-main.html';
};

createButton.onclick = function () {
    xhr.open('POST', url);

    let result = JSON.stringify({
        "event_name": eventTitle.value,
        "date_of_event": dateStart.value,
        "end_of_event": dateEnd.value,
        "address": locationField.value,
        "coordinates": coordinates,
        "responsible_club": respClub.value,
        "responsible_trainer": leadCoach.value,
        "max_rang": maxRang.value,
        "location_map": locationMap,
        "contacts": contacts
    });

    console.log(result);
    xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'));
    xhr.send(result);
}
