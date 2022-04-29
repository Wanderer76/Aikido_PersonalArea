import {eventSlug} from "./get-event-info-script.js";

let storage = window.sessionStorage;
const userToken = storage.getItem('user_token');

let eventName = eventSlug;
let downloadUrl = `http://localhost:8000/api/v1/events/file/download/${eventName}/`;
let downloadButton = document.getElementById('download');
let downloader = new XMLHttpRequest();

downloadButton.onclick = function () {
    downloader.open('GET', downloadUrl);
    downloader.setRequestHeader('Authorization', 'Token ' + userToken);
    downloader.send();
}

downloader.onload = function () {
    if ((downloader.status >= 200 && downloader.status < 300)) {
        window.open(downloadUrl);
    } else {
        alert(JSON.parse(downloader.response).result);
    }
};

