let storage = window.sessionStorage;
let baseInfoRequest = new XMLHttpRequest();
getRequest('http://localhost:8000/api/v1/events/base_for_trainer/' + storage.getItem("slug") + '/', setInfoToHeader);

function setInfoToHeader(data) {
    console.log(data);
    let info = JSON.parse(data);
    let output = document.createElement('div');
    let beforeInsertingElement = document.getElementById('buttons-block');
    output.classList.add('container');
    output.classList.add('seminar-info');
    output.innerHTML =
                '<h1 id="event-name">' + info.event_name + '</h1>\n' +
        '        <p>Дата: <span class="changeable-params">' + createDateOutput(info.date_of_event, info.end_of_event) + '</span></p>\n' +
        '        <p>Место: <span class="changeable-params">'+ info.address +'</span></p>\n' +
        '        <p>Количество заявленных участников: <span class="changeable-params">'+ info.count+ '</span></p>\n' +
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