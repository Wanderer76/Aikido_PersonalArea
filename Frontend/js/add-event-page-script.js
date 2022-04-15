import {coordinates} from "./add-event-map-script.js";
import {createSchedule} from "./add-event-schedule-script.js";

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

let posterImage = document.getElementById('event-poster');

let orgName = document.getElementById('org-name');
let orgPhone = document.getElementById('org-phone');
let orgEmail = document.getElementById('org-email');

function getCouchOffset(couchXOffset, couchYOffset) {
    const couchImg = {
        x_offset: couchXOffset.value,
        y_offset: couchYOffset.value
    }
    console.log(couchImg);
    return JSON.stringify(couchImg, null);
}

function getLogoOffset(logoXOffset, logoYOffset) {
    const logoImg = {
        x_offset: logoXOffset.value,
        y_offset: logoYOffset.value
    }
    console.log(logoImg);
    return JSON.stringify(logoImg, null);
}

function getContacts(orgName, orgPhone, orgEmail) {
    const contacts = {
        org_name: orgName.value,
        org_phone: orgPhone.value,
        org_email: orgEmail.value
    };
    console.log(contacts);
    return JSON.stringify(contacts, null);;
}

const url = "http://127.0.0.1:8000/api/v1/events/create/";
let xhr = new XMLHttpRequest();
xhr.responseType = 'json';
let storage = window.sessionStorage;
let token = storage.getItem('user_token');

xhr.onreadystatechange = function () {
    let data = xhr.response;
    console.log(data);
    //location.href = '../html/admin-page-main.html';
};

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
    formData.append("coach_offset", getCouchOffset(couchXOffset, couchYOffset));
    formData.append("logo_img", logoImage.files[0]);
    formData.append("logo_offset", getLogoOffset(logoXOffset, logoYOffset));
    formData.append("poster", posterImage.files[0]);
    formData.append("contacts", getContacts(orgName, orgPhone, orgEmail));

    console.log(formData);
    xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'));
    xhr.send(formData);
}

