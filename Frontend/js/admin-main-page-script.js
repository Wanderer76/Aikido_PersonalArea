let url = "http://localhost:8000/api/v1/admin/seminar_statistic/";
let xhr = new XMLHttpRequest();
let storage = window.sessionStorage;
let data;
let comingActivitiesHeader = document.getElementById('coming-activities-header');
let previewActivitiesHeader = document.getElementById('preview-activities-header');
let received = false;

xhr.open('GET', url);
xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'))
xhr.send();

xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        data = xhr.response;
        console.log(data);
        addDataToTable(data, comingActivitiesHeader, 'upcoming');
        addDataToTable(data, previewActivitiesHeader, 'past');
        buttonsFunc();
    }
}

function buttonsFunc() {
    let buttons = document.querySelectorAll('.more_details');
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].onclick = function () {
            console.log(i)
        }
    }
}

function addDataToTable(data, tagAfterInserting, tag) {
    let activities = JSON.parse(data);
    let array;

    if (tag == 'upcoming')
        array = activities.upcoming;
    else array = activities.past;

    if (array.length == 0) {
        return;
    }

    for (var i = 0; i < array.length; i++) {
        let activity = array[i];
        let output = document.createElement('div');
        output.classList.add('row');
        output.classList.add('align-items-center');
        output.innerHTML =
            '   <div class="col" id="name'+ i +'">' + activity.event_name + '</div>' +
            '   <div class="col date">\n' +
            '       '+ createDateOutput(activity.date_of_event, activity.end_of_event) + '\n' +
            '   </div>\n' +
            '   <div class="col">\n' +
            '       г.'+ activity.city +'\n' +
            '   </div>\n' +
            '   <div class="col">\n' + activity.responsible_club +
            '   </div>\n' +
            '   <div class="col">\n' +
            '       <button type="button" name="more_details" class="more_details" id="more-button-'+i+'">Подробнее</button>\n' +
            '   </div>\n';

        tagAfterInserting.parentElement.insertBefore(output, tagAfterInserting.nextSibling);
    }
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