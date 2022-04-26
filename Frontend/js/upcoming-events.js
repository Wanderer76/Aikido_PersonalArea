// let xhr = new XMLHttpRequest();
// const url = 'http://localhost:8000/api/v1/events/upcoming_list/';
// let storage = window.sessionStorage;
// xhr.open('GET', url);
// xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'))
// xhr.send();
//
// xhr.onreadystatechange = function() {
//     if (this.readyState == 4 && this.status == 200) {
//         data = xhr.response;
//         console.log(data);
//         createEvents(xhr.response);
//     }
// }

getRequest('http://localhost:8000/api/v1/events/upcoming_list/', createEvents);

function createEvents(data) {
    let events = JSON.parse(data);
    for (let event of events.reverse()) {
        console.log(event);
        let card = document.createElement('a');
        card.classList.add('card-link');
        fillCard(card, event);
        let header = document.querySelector('h1')
        header.parentElement.insertBefore(card, header.nextSibling);
    }
}

function fillCard(cardNode, eventInfo) {
    let html = '<div class="bordered-container card">\n' +
        '                    <div class="ro">\n' +
        '                        <img src="'+ eventInfo.poster +'">\n' +
        '                        <div class="inf-list">\n' +
        '                            <p class="club_name">'+ eventInfo.event_name +'</p>\n' +
        '                            <p class="date">'+ createDateOutput(eventInfo.date_of_event, eventInfo.end_of_event) +'</p>\n' +
        '                            <p class="city">'+ eventInfo.address +'</p>\n' +
        '                            <button type="button" class="moreBut" name="edit" onclick="goToEventPage(\''+ eventInfo.slug +'\')">Подробнее</button>\n' +
        '                        </div>\n' +
        '                    </div>\n' +
        '                </div>'
    cardNode.innerHTML = html;
}

function goToEventPage(slug) {
    window.sessionStorage.getItem('event_slug', slug);
    location.href = '../html/event-page.html';
}

function createDateOutput(date1, date2) {
    var startDate = new Date(date1);
    var endDate = new Date(date2);
    if (startDate.getMonth() == endDate.getMonth() && startDate.getFullYear() == endDate.getFullYear())
        return startDate.getDate() + " - " + endDate.getDate() + " " + endDate.toLocaleString('default', {month: 'long'}) + " "+ endDate.getFullYear();
    else if (startDate.getMonth() !== endDate.getMonth() && startDate.getFullYear() == endDate.getFullYear())
        return startDate.getDate() + " " + startDate.toLocaleString('default', {month: 'long'}) + " - " +
            endDate.getDate() + " " + endDate.toLocaleString('default', {month: 'long'}) + " " + startDate.getFullYear();
    else return startDate.getDate() + " " +startDate.toLocaleString('default', {month: 'long'}) + " " + startDate.getFullYear() + " - " +
            endDate.getDate() + " " + endDate.toLocaleString('default', {month: 'long'}) + " " + endDate.getFullYear();
}