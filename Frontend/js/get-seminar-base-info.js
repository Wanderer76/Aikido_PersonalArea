let storage = window.sessionStorage;
let baseInfoRequest = new XMLHttpRequest();
SendSeminarInfoRequest('http://localhost:8000/api/v1/admin/event_statistic/' + storage.getItem("activityName") + '/', baseInfoRequest);

function SendSeminarInfoRequest(url) {

    baseInfoRequest.open('GET', url);
    baseInfoRequest.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'))
    baseInfoRequest.send();
}

baseInfoRequest.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        let data = baseInfoRequest.response;
        setInfoToHeader(data);
    }
}

function setInfoToHeader(data) {
    let info = JSON.parse(data).result;
    let output = document.createElement('div');
    let beforeInsertingElement = document.getElementById('buttons-block');
    output.classList.add('container');
    output.classList.add('seminar-info');
    output.innerHTML =
                '<h1 id="event-name">' + info.event_name + '</h1>\n' +
        '        <p>Дата: <span class="changeable-params">' + createDateOutput(info.date_of_event, info.end_of_event) + '</span></p>\n' +
        '        <p>Место: <span class="changeable-params">'+ info.city +'</span></p>\n' +
        '        <p>Ответственный клуб: <span class="changeable-params">'+ info.responsible_club +'</span></p>' +
        '        <p>Ответственный тренер: <span class="changeable-params">' + info.responsible_trainer + '</span></p>' +
        '        <p>Количество заявленных участников: <span class="changeable-params">111</span></p>\n' +
        '        <p>Окончание записи через сайт: <span class="changeable-params">'+ info.end_record_date +'</span></p>';
    beforeInsertingElement.parentElement.insertBefore(output, beforeInsertingElement);
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