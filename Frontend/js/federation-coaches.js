let xhr = new XMLHttpRequest();
const url = 'http://localhost:8000/api/v1/account/trainers/';
let storage = window.sessionStorage;
let data;
xhr.open('GET', url);
xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'))
xhr.send();

xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        data = xhr.response;
        console.log(data);
        fillCoachesList(xhr.response);
    }
}
function fillCoachesList(data){
    let coaches = JSON.parse(data);
    let table = document.querySelector('.bordered');
    for (let trainer in coaches){
        let row = document.createElement('div');
        row.classList.add('row');
        row.classList.add('inf-coaches');
        row.innerHTML =
            '<div class="col bordered-2">' + trainer.surname + ' ' + trainer.name + ' ' + trainer.second_name + '</div>' +
            '<div class="col bordered-2">' + trainer.birthdate + '</div>' +
            '<div class="col bordered-2">' + parseKu(trainer.ku) + '</div>' +
            '<div class="col">' + trainer.attestation_date + '</div>';
        table.parentElement.insertBefore(row, table.nextSibling);
    }

}
function parseKu(ku){
    if (ku < 10){
        return ku + 'кю';
    }
    else return  ku % 10 + 'дан';
}
