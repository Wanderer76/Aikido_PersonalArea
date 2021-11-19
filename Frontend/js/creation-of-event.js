const url = "http://localhost:8000/api/v1/events/create/";
let xhr = new XMLHttpRequest();
xhr.responseType = 'json';
let storage = window.sessionStorage;
let token = storage.getItem('user_token');

let create_button = document.getElementById('create');
let event_title = document.getElementById('event_title');
let date_start = document.getElementById('date_start');
let date_end = document.getElementById('date_end');
let locatio = document.getElementById('location');
let resp_club = document.getElementById('resp_club');

xhr.onreadystatechange = function () {
    let data = xhr.response;
    console.log(data);
};

create_button.onclick = function () {

    //let lead_coach = document.getElementById('lead_coach').value;
    xhr.open('POST', url);

    let result = JSON.stringify({
        "event_name": event_title.value,
        "start_record_date": date_start.value,
        "end_record_date": "2020-05-13",
        "date_of_event": date_end.value,
        "city": locatio.value,
        "responsible_club": resp_club.value
    });

    console.log(result);
    xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'))
    xhr.send(result);
}