let xhr = new XMLHttpRequest();
const url = 'http://localhost:8000/api/v1/events/upcoming_list/';
let storage = window.sessionStorage;
xhr.open('GET', url);
xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'))
xhr.send();

xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        data = xhr.response;
        console.log(data);
        createEvents(xhr.response);
    }
}

function createEvents(data) {
    let events = JSON.parse(data);
    console.log(events);
    for (let event of events) {
        console.log(event);
        let card = document.createElement('div');
        card.classList.add('card');
        card.classList.add('bordered');
        fillCard(card, event);
    }
}

function fillCard(cardNode, eventInfo) {
    let html = '<div class="ev-ic">' +
        '<img src="' + eventInfo['poster'] + '">' +
        '<div class="inf-list">' +
        '<p class="event-name">' + eventInfo['event_name'] + '</p>' +
        '<p class="event-dates">г.' + parseDates(eventInfo['date_of_event'], eventInfo['end_of_event']) +  '</p>' +
        '<p class="event-area">' + eventInfo['address'] + '</p>' +
        '<button type="button" class="more_details" name="more_details">Подробнее</button>';
    html += '</div>\n' +
        '</div>'
    cardNode.innerHTML = html;
}

function parseDates(date_of_event, end_of_event){
    let first = new Date(date_of_event);
    let second = new Date(end_of_event);
    return first.getDay() + '-' + second.getDay() + ' ' + first.getMonth() + ' ' + first.getFullYear();
}