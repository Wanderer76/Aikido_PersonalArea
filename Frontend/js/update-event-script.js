import {createFormData} from "./send-event-info-script.js";
import {eventSlug} from "./get-event-info-script.js";

let xhr = new XMLHttpRequest();
xhr.responseType = 'json';
let storage = window.sessionStorage;
const userToken = storage.getItem('user_token');

xhr.onreadystatechange = function () {
    // if (xhr.status >= 200 && xhr.status < 300) {
    //     let data = xhr.response;
    //     //location.href = '../html/admin-page-main.html';
    // } else {
    //     alert('Не все поля заполнены верно!');
    // }
    let data = xhr.response;
    //location.href = '../html/admin-page-main.html';
};

const editButton = document.getElementById('edit');

editButton.onclick = function () {
    xhr.open('PATCH', `http://127.0.0.1:8000/api/v1/events/update/${eventSlug}/`);
    const formData = createFormData();

    xhr.setRequestHeader('Authorization', 'Token ' + userToken);
    xhr.send(formData);
}

