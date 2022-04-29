import {createFormData} from "./send-event-info-script.js";
import {eventSlug} from "./get-event-info-script.js";

let xhr = new XMLHttpRequest();
xhr.responseType = 'json';
let storage = window.sessionStorage;
const userToken = storage.getItem('user_token');

xhr.onload = function () {
    if ((xhr.status >= 200 && xhr.status < 300)) {
        alert('Мероприятие успешно отредактировано.');
        location.href = '../html/admin-page-main.html';
    } else {
        console.log(xhr.response);
        alert(`Вы упустили некоторые поля или заполнили их неверно! \n Статус ответа: ${xhr.status}. \n ${xhr.response} \n Обратите внимание! \n Вы не можете создать мероприятие с одним и тем же названием, если оно имеется в списке мероприятий. \n Файлы изображений можно заменить при необходимости. \n Все текстовые поля, ввод дат и выпадающие списки являются обязательными. \n Расписание соревнований можно оставить пустым до дальнейшего редактирования.`);
    }
};

const editButton = document.getElementById('edit');

editButton.onclick = function () {
    xhr.open('PATCH', `http://127.0.0.1:8000/api/v1/events/update/${eventSlug}/`);
    const formData = createFormData();

    xhr.setRequestHeader('Authorization', 'Token ' + userToken);
    xhr.send(formData);
}

