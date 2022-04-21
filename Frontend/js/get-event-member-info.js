let eventMemberRequest = new XMLHttpRequest();
eventMemberRequest.responseType = 'json';

let studentsInfoRequest = new XMLHttpRequest();
studentsInfoRequest.responseType = 'json';
const stud_url = "http://localhost:8000/api/v1/account/trainer/students/";

let studentList;
let eventCheckedMemmbers;
let havePreviewRequest;
LoadMemberEventInfo();

function LoadMemberEventInfo() {
    let urlEventInfo = 'http://localhost:8000/api/v1/events/trainer/requests/'+ storage.getItem("slug") +'/';
    eventMemberRequest.open('GET', urlEventInfo);
    eventMemberRequest.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'))
    eventMemberRequest.send();
}

eventMemberRequest.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        if (this.response.length == 0)
            havePreviewRequest = false;
        else {
            havePreviewRequest = true;
            eventCheckedMemmbers = eventMemberRequest.response;
            console.log(eventCheckedMemmbers);
        }
        getTrainerStudents();
    }
}

studentsInfoRequest.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        studentList = this.response['список учеников'];
        showTrainerStudents(studentList);
        if (havePreviewRequest) changeAplication();
    }
    // console.log(this.response);
}

function changeAplication() {
    console.log('change');
    checkStudentsFromPreviewAplication(eventCheckedMemmbers);
    addNewMembersFromPreviewAplication(eventCheckedMemmbers);
}

function checkStudentsFromPreviewAplication(eventCheckedMembers) {
    let checkboxes = document.querySelectorAll('.checkbox');
    for (let i=0; i<checkboxes.length; i++)
        checkStudent(checkboxes[i], eventCheckedMembers);
}

function checkStudent(checkbox, eventCheckedMembers) {
    let studentId = checkbox.parentElement.parentElement.getElementsByTagName("td")[0].textContent;
    for (let i=0; i< eventCheckedMembers.length; i++) {
        if (('#' + eventCheckedMembers[i].member_id) == studentId) {
            checkbox.checked = true;
        }
    }
}

function addNewMembersFromPreviewAplication(eventCheckedMembers) {
    let defRow = document.getElementById('default-row');
    for (let i=0; i< eventCheckedMembers.length; i++) {
        if (!checkMemberInListByID(studentList, eventCheckedMembers[i].member_id)) {
            let output = document.createElement('tr');
            output.innerHTML =
            '<td></td>' +
            '<td>'+ eventCheckedMembers[i].name + ' ' + eventCheckedMembers[i].surname + ' ' + eventCheckedMembers[i].second_name +'</td>' +
            '<td>'+ setDateFormat(eventCheckedMembers[i].birthdate) +'</td>' +
            '<td></td>' +
            '<td class="checkbox-cell"><input type="checkbox" class="checkbox" checked></td>';
            defRow.parentElement.insertBefore(output, defRow);
        }
    }
}

function checkMemberInListByID(list, id) {
    for (let i=0; i<list.length; i++) {
        if (list[i].id == null)
            continue;
        if (list[i].id == id)
            return true;
    }
    return false;
}


function getTrainerStudents() {
    studentsInfoRequest.open("GET", stud_url);
    studentsInfoRequest.setRequestHeader('Authorization', 'Token ' + window.sessionStorage.getItem('user_token'));
    studentsInfoRequest.send();
}


function showTrainerStudents(studData) {
    let defRow = document.getElementById('default-row');
    if (studData.length == 0) {
        defRow.children[0].textContent = 'Нет участников. Добавьте новичков!';
        defRow.parentElement.removeChild(defRow.parentElement.children[0]);
        return;
    }
    for (let i = 0; i < studData.length; i++) {
        let output = document.createElement('tr');
        output.innerHTML =
        '<td>#'+ studData[i].id +'</td>' +
        '<td>'+ studData[i].name + ' ' + studData[i].surname +'</td>' +
        '<td>'+ setDateFormat(studData[i].birthdate) +'</td>' +
        '<td>' +
            '<div class="degree ku-'+ studData[i].ku +'">'+ studData[i].ku+' кю <br><span  class="dateInBlock">'+ setDateFormat(studData[i].attestation_date) +'</span></div>' +
        '</td>' +
        '<td class="checkbox-cell"><input type="checkbox" class="checkbox"></td>';
        defRow.parentElement.insertBefore(output, defRow);
    }
}


function setDateFormat(strDate) {
    let date = new Date(strDate);

    let month = date.getMonth()+1;
    if (month < 10) {month = '0' + month};

    let day = date.getDate()
    if (day < 10) {day = '0' + day}
    return day + '.' + month + '.' + date.getFullYear();
}

