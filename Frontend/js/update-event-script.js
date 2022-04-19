//для обновления мероприятия

import {createFormData} from "./send-event-info-script.js";
import {eventSlug} from "./get-event-info-script.js";

let xhr = new XMLHttpRequest();
xhr.responseType = 'json';
let storage = window.sessionStorage;
let token = storage.getItem('user_token');

xhr.onreadystatechange = function () {
    let data = xhr.response;
    //location.href = '../html/admin-page-main.html';
};

const editButton = document.getElementById('edit');

editButton.onclick = function () {
    xhr.open('PATCH', `http://127.0.0.1:8000/api/v1/events/update/${eventSlug}/`);
    const formData = createFormData();

    xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'));
    xhr.send(formData);
}

