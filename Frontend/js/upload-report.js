import {eventSlug} from "./get-event-info-script.js";

let storage = window.sessionStorage;
const userToken = storage.getItem('user_token');

let uploadButton = document.getElementById('upload');
let uploadUrl = `http://localhost:8000/api/v1/events/file/upload/${eventSlug}/`;
let uploader = new XMLHttpRequest();

uploader.onreadystatechange = state => { console.log(uploader.response); }

uploadButton.onchange = function () {
    let file = document.getElementById('upload').files[0];
    let fileName = eventSlug + '.' + file.name.split('.').pop();
    console.log('fileName is ', fileName);
    let formData = new FormData();
    formData.append(eventSlug, file, eventSlug + '.' + file.name.split('.').pop());

    uploader.open('PUT', uploadUrl);
    uploader.setRequestHeader('Authorization', 'Token ' + userToken);
    uploader.setRequestHeader('Content-Disposition', `attachment; filename="${fileName}"`);
    uploader.send(formData);
}
