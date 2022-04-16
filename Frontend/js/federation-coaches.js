// let xhr = new XMLHttpRequest();
// const url = 'http://localhost:8000/api/v1/account/trainers/';
// let storage = window.sessionStorage;
// let data;
// xhr.open('GET', url);
// xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'))
// xhr.send();
//
// xhr.onreadystatechange = function() {
//     if (this.readyState == 4 && this.status == 200) {
//         data = xhr.response;
//         console.log(data);
//         fillCoachesList(xhr.response);
//     }
// }

getRequest('http://localhost:8000/api/v1/account/trainers/', fillCoachesList)

function fillCoachesList(data){
    let coaches = JSON.parse(data);
    console.log(coaches);
    for (let trainer of coaches){
        console.log(trainer);
        let row = document.createElement('div');
        row.classList.add('row');
        row.classList.add('inf-coaches');
        row.setAttribute('onclick', 'goToEditPage('+ trainer['id']+  ')');
        let innerEl = document.getElementsByClassName('row')[document.getElementsByClassName('row').length-1];
        row.innerHTML =
            '<div class="col bordered-2">' + trainer['surname'] + ' ' + trainer['name'] + ' ' + trainer['second_name'] + '</div>' +
            '<div class="col bordered-2">' + setDateFormat(trainer['birthdate']) + '</div>' +
            '<div class="col bordered-2">' + parseKu(trainer['ku']) + '</div>' +
            '<div class="col">' + setDateFormat(trainer['attestation_date']) + '</div>';
        innerEl.parentElement.insertBefore(row, innerEl.nextSibling);
    }

}
function parseKu(ku){
    if (ku === '')
        return 'Не указано';
    if (ku < 10){
        return ku + 'кю';
    }
    else return  ku % 10 + 'дан';
}

function setDateFormat(strDate) {
    let date = new Date(strDate);

    let month = date.getMonth()+1;
    if (month < 10) {month = '0' + month};

    let day = date.getDate()
    if (day < 10) {day = '0' + day}
    return day + '.' + month + '.' + date.getFullYear();
}

function goToEditPage(id) {
    window.sessionStorage.setItem('trainer_id', id);
    location.href = "../html/edit-trainer.html";
}

