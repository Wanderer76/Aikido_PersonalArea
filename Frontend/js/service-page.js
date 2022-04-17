const url = "http://localhost:8000/api/v1/account/profile/";
let trainer_xhr = new XMLHttpRequest();
trainer_xhr.responseType = 'json';
let storage = window.sessionStorage;
let token = storage.getItem('user_token');

trainer_xhr.onreadystatechange = function () {
    console.log(trainer_xhr.response);
    setTrainerBaseInfo(trainer_xhr.response);
}
trainer_xhr.open("GET", url, true);
trainer_xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'));
trainer_xhr.send();

function setTrainerBaseInfo(data){
    document.getElementById('name').textContent = data.name;
    document.getElementById('surname').textContent = data.surname;
    document.getElementById('id').textContent = 'ID #' + data.id;
    document.getElementById('region').textContent = data.region;
    document.getElementById('city').textContent = data.seminars[0].city;
    document.getElementById('club').textContent = data.club;
    document.getElementById('stud-count').textContent = data.members;
    document.getElementById('validity').textContent = '';
}


