let studentsInfoRequest = new XMLHttpRequest();
studentsInfoRequest.responseType = 'json';
const stud_url = "http://localhost:8000/api/v1/account/trainer_students/";

getTrainerStudents();
function getTrainerStudents() {
    studentsInfoRequest.open("GET", stud_url);
    studentsInfoRequest.setRequestHeader('Authorization', 'Token ' + window.sessionStorage.getItem('user_token'));
    studentsInfoRequest.send();
}


studentsInfoRequest.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        fillTable(this.response['список учеников']);
    }
}

function fillTable(studList) {
    let header = document.getElementById('header');
    if (studList.length == 0) return;
    for (let i = 0; i < studList.length; i++) {
        let output = document.createElement('tr');
        output.innerHTML =
            '<td>#'+ studList[i].id+'</td>' +
            '<td className="border-cell">'+ studList[i].name +'</td>' +
            '<td className="border-cell">'+ studList[i].surname +'</td>' +
            '<td>'+ studList[i].password +'</td>';
        header.parentElement.insertBefore(output, header.nextSibling);
    }
}

