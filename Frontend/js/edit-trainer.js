getRequest("http://localhost:8000/api/v1/account/trainers/base/" + sessionStorage.getItem('trainer_id') + "/", fillInputs);

function fillInputs(data) {
    console.log("Получены данные")
    console.log(data)
    let trainerInfo = JSON.parse(data);

    document.getElementById('surname').value = trainerInfo.surname;
    document.getElementById('name').value = trainerInfo.name;
    document.getElementById('second-name').value = trainerInfo.second_name;
    fillDate(document.getElementById('birthdate'), trainerInfo.birthdate);
    document.getElementById('rank-selector').value = trainerInfo.received_ku;
    fillDate(document.getElementById('attestation-date'), trainerInfo.attestation_date);
    document.getElementById('club-selector').value = trainerInfo.club;
    document.getElementById('event-name').value = trainerInfo.event_name;
}


function fillDate(textNode, info) {
    textNode.type = 'date';
    textNode.value = info;
}


function hideAcceptBlock() {
    let acceptBlock = document.getElementById('accept-block');
    acceptBlock.classList.add('hidden');
}


function deleteCoach() {
    let url = 'http://localhost:8000/api/v1/account/modificate_trainer/'+ sessionStorage.getItem('trainer_id') +'/';
    let id = sessionStorage.getItem('trainer_id');
    let acceptBlock = document.getElementById('accept-block');
    acceptBlock.classList.remove('hidden');
    let acceptBut = document.getElementsByClassName('accept-button')[0];
    acceptBut.onclick = function () {
        postWithoutAnswer(url, undefined, "DELETE", function () {location.href = '../html/federation_coaches.html'});
        console.log('Тренер должен удалиться');
    }
}


function sendEditInfo() {
    let sendingData = getAllInfo(false);
    let url = 'http://localhost:8000/api/v1/account/modificate_trainer/'+ sessionStorage.getItem('trainer_id') +'/';

    if (checkInputsInSendingData(sendingData)) {
        console.log("Отправка файла...")
        console.log(JSON.stringify(sendingData));
        postWithoutAnswer(url, JSON.stringify(sendingData), "PATCH", function () {location.href = '../html/federation_coaches.html'}, 'json');

    }
    else {
        document.getElementById('error-message').classList.remove('hidden');
    }
}