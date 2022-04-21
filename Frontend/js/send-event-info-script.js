import {coordinates} from "./add-event-map-script.js";
import {createSchedule} from "./add-event-schedule-script.js";

const createButton = document.getElementById('create');

let xhr = new XMLHttpRequest();
xhr.responseType = 'json';
let storage = window.sessionStorage;
let token = storage.getItem('user_token');

xhr.onload = function () {
    if ((xhr.status >= 200 && xhr.status < 300)) {
        location.href = '../html/admin-page-main.html';
    } else {
        console.log(xhr.response);
        alert(`Вы упустили некоторые поля или заполнили их неверно! \n Статус ответа: ${xhr.status}. \n Обратите внимание! \n Вы не можете создать мероприятие с одним и тем же названием, если оно имеется в списке мероприятий. \n Поля загрузки изображений: фото тренера, логотипа клуба и афишы являютя обязательными. \n Все текстовые поля, ввод дат и выпадающие списки являются обязательными. \n Расписание соревнований можно оставить пустым до дальнейшего редактирования.`);
    }
};

createButton.onclick = function () {

    xhr.open('POST', "http://127.0.0.1:8000/api/v1/events/create/");
    const formData = createFormData();
    xhr.setRequestHeader('Authorization', 'Token ' + token);
    xhr.send(formData);
}

export function createFormData() {
    const eventTitle = document.getElementById('event-name');
    const dateStart = document.getElementById('date-start');
    const dateEnd = document.getElementById('date-end');
    const locationField = document.getElementById('event-location');
    const respClub = document.getElementById('resp-club-select');
    const leadCoach = document.getElementById('lead-coach');
    const maxRang = document.getElementById('max-rang-select');

    const couchImage = document.getElementById('coach-icon');
    const couchXOffset = document.getElementById('coach-x-offset');
    const couchYOffset = document.getElementById('coach-y-offset');

    const logoImage = document.getElementById('logo-icon');
    const logoXOffset = document.getElementById('logo-x-offset');
    const logoYOffset = document.getElementById('logo-y-offset');

    const posterImage = document.getElementById('event-poster');

    const orgName = document.getElementById('org-name');
    const orgPhone = document.getElementById('org-phone');
    const orgEmail = document.getElementById('org-email');

    const schedule = JSON.stringify(createSchedule(), null);

    function getCouchOffset(couchXOffset, couchYOffset) {
        const couchImg = {
            x_offset: couchXOffset.value,
            y_offset: couchYOffset.value
        }

        return JSON.stringify(couchImg, null);
    }

    function getLogoOffset(logoXOffset, logoYOffset) {
        const logoImg = {
            x_offset: logoXOffset.value,
            y_offset: logoYOffset.value
        }

        return JSON.stringify(logoImg, null);
    }

    function getContacts(orgName, orgPhone, orgEmail) {
        const contacts = {
            org_name: orgName.value,
            org_phone: orgPhone.value,
            org_email: orgEmail.value
        };

        return JSON.stringify(contacts, null);
    }

    let formData = new FormData();

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

    return formData;
}

