let seminar_url = "http://localhost:8000/api/v1/events/event_list/";
getRequest(seminar_url, fillSeminarTables);

let num=0;

function sendActivityName(button, action, slug) {
    let buttonNum = button.id.split('-')[2];
    sessionStorage.setItem("slug", slug);
    if (action == 'download') {
        let seminarName = window.sessionStorage.getItem("activityName");
        let downloadUrl = 'http://localhost:8000/api/v1/admin/seminar/download/'+ seminarName + '/';
        let downloader = new XMLHttpRequest();
        let data;
        downloader.open('GET', downloadUrl);
        downloader.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'))
        downloader.send();
        console.log("downloading...");

        downloader.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                data = downloader.response;
                window.open(data);
            }
        }
    }
    else
        location.href = "../html/create_aplication.html";
}

function fillSeminarTables(data) {
    let comingActivitiesHeader = document.getElementById('coming-activities-header');
    let previewActivitiesHeader = document.getElementById('preview-activities-header');
    addDataToTable(data, comingActivitiesHeader, 'upcoming');
    addDataToTable(data, previewActivitiesHeader, 'past');

}

function addDataToTable(data, tagAfterInserting, tag) {
    let activities = JSON.parse(data);
    console.log(activities)
    let array;

    if (tag == 'upcoming')
        array = activities.upcoming;
    else array = activities.past;

    if (array.length == 0) {
        return;
    }

    for (var i = 0; i < array.length; i++) {
        let activity = array[i];
        let output = document.createElement('tr');
        if (tag == 'upcoming')
            output.innerHTML =
           ' <tr>' +
               ' <td>'+ createDateOutput(activity.date_of_event, activity.end_of_event) +'</td>' +
               '<td class ="bordered-3" id="name-'+ num +'">'+ activity.event_name +'</td>'+
               ' <td class="bordered-3">'+ activity.city +'</td>' +
                '<td class="bordered-3">'+ activity.responsible_club +'</td>' +
                '<td class="bordered-3">' +
                   ' <button type="button" name="apply" class="apply" id="more-button-'+ num + '"  onclick="sendActivityName(this, \'apply\', \'' + activity.slug + '\')">Подать \ Изменить заявку' +
                   ' </button>' +
                '</td>' +
            '</tr>';
        else  output.innerHTML =
            ' <tr>' +
            ' <td>'+ createDateOutput(activity.date_of_event, activity.end_of_event) +'</td>' +
            '<td class ="bordered-3" id="name-'+ num +'">'+ activity.event_name +'</td>'+
            ' <td class="bordered-3">'+ activity.city +'</td>' +
            '<td class="bordered-3">'+ activity.responsible_club +'</td>' +
            '<td class="bordered-3">' +
            ' <button type="button" name="download_sheet" class="download_sheet" id="more-button-'+ num + '"  onclick="sendActivityName(this, \'download\')">Скачать ведомость' +
            ' </button>' +
            '</td>' +
            '</tr>';


        tagAfterInserting.parentElement.insertBefore(output, tagAfterInserting.nextSibling);
        num++;
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