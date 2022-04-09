import {createSchedule} from "./add-event-schedule";

// Скрипт для формы загрузки
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
    let myMap = new ymaps.Map('map', {
        center: [56.838048312714704,60.60364972721357],
        zoom: 16,
        controls: []
    });

    let searchControl = new ymaps.control.SearchControl({
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

//formData
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

let couchImg = {
    x_offset: couchXOffset.value,
    y_offset: couchYOffset.value
}
const couchOffset = JSON.stringify(couchImg, null);

let logoImg = {
    x_offset: logoXOffset.value,
    y_offset: logoYOffset.value
}
const logoOffset = JSON.stringify(logoImg, null);

let contact = {
    org_name: orgName.value,
    org_phone: orgPhone.value,
    org_email: orgEmail.value
};
const contacts = JSON.stringify(contact, null);

const url = "http://127.0.0.1:8000/api/v1/events/create/";
let xhr = new XMLHttpRequest();
xhr.responseType = 'json';
let storage = window.sessionStorage;
let token = storage.getItem('user_token');

xhr.onreadystatechange = function () {
    let data = xhr.response;
    console.log(data);
    location.href = '../html/admin-page-main.html';
};

let poster = new File([""], "../assets/empty-poster.png")

createButton.onclick = function () {

    xhr.open('POST', url);

    let formData = new FormData();

    let schedule = JSON.stringify(createSchedule(), null);

    formData.append("event_name", eventTitle.value);
    formData.append("date_of_event", dateStart.value);
    formData.append("end_of_event", dateEnd.value);
    formData.append("address", locationField.value);
    formData.append("coordinates", coordinates);
    formData.append("responsible_club", respClub.value);
    formData.append("responsible_trainer", leadCoach.value);
    formData.append("max_rang", maxRang.value);
    formData.append("schedule", schedule);
    formData.append("couch_img", couchImage.files[0]);
    formData.append("coach_offset", couchOffset);
    formData.append("logo_img", logoImage.files[0]);
    formData.append("logo_offset", logoOffset);
    formData.append("poster", poster);
    formData.append("contacts", contacts);

    console.log(formData);
    xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'));
    xhr.send(formData);
}

