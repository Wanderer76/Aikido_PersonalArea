const url = "http://localhost:8000/api/v1/events/create/";
let xhr = new XMLHttpRequest();
xhr.responseType = 'json';
let storage = window.sessionStorage;
let token = storage.getItem('user_token');

let create_button = document.getElementById('create');
let event_title = document.getElementById('event_title');
let date_start = document.getElementById('date_start');
let date_end = document.getElementById('date_end');
let location_field = document.getElementById('location');
let resp_club = document.getElementById('resp_club');
let lead_coach = document.getElementById('lead_coach');
console.log("Enter")

xhr.onreadystatechange = function () {
    let data = xhr.response;
    console.log(data);
};

create_button.onclick = function () {

    //let lead_coach = document.getElementById('lead_coach').value;
    xhr.open('POST', url);

    let result = JSON.stringify({
        "event_name": event_title.value,
        "date_of_event": date_start.value,
        "end_of_event": date_end.value,
        "city": location_field.value,
        "responsible_club": resp_club.value,
        "responsible_trainer": lead_coach.value
    });

    console.log(result);
    xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'));
    xhr.send(result);
}