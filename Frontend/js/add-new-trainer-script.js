getRequest('http://localhost:8000/api/v1/account/candidates/trainers/', fillTrainerSelector);
getRequest('http://localhost:8000/api/v1/clubs/get_clubs/', fillClubSelector)

function fillTrainerSelector(data) {
    let trainers = JSON.parse(data);
    let selector = document.getElementById('coach-selector');
    for (let trainer of trainers) {
        selector.innerHTML += '<option value="'+ trainer['id'] + '">'+ trainer['name'] + ' ' + trainer['surname'] + ' ' + trainer['second_name']  + ' #' + trainer['id'] +'</option>';
    }
}

function fillClubSelector(data) {
    let clubs = JSON.parse(data);
    console.log(clubs);
    let selector = document.getElementById('club-selector');
    for (let club of clubs) {
        selector.innerHTML += '<option value="'+ club['name'] + '">'+ club['name'] +'</option>';
    }
}



function getAllInfo(flag) {

    if (flag && document.getElementById('coach-selector').value !== 'none') {
        return {'id' : document.getElementById('coach-selector').value}
    }
    else {
        return  {'surname' : document.getElementById('surname').value,
                      'name' : document.getElementById('name').value,
                      'second_name' : document.getElementById('second-name').value,
                      'birthdate' : document.getElementById('birthdate').value,
                      'received_ku' : document.getElementById('rank-selector').value,
                      'club' : document.getElementById('club-selector').value,
                      'event_name' : document.getElementById('event-name').value,
                      'attestation_date': document.getElementById('attestation-date').value
        }

    }
}

function hideErrorMessage(node, defaultValue) {
    document.getElementById('error-message').classList.add('hidden');
    if (node.value === '') {
        changeType(node, 'text', defaultValue)
    }

}

function checkInputsInSendingData(sendingData) {
    return (sendingData['surname'] !== '' && sendingData['name'] !== '' && sendingData['second_name'] !== '' &&
        sendingData['birthdate'] !== '' && sendingData['rank'] !== 'none' && sendingData['club'] !== 'none' &&
        sendingData['last_event'] !== '')
}

function sendInfo() {
    let sending_data = getAllInfo(true);
    if (sending_data['id'] !== 'none' && sending_data['id'] !== undefined) {
            console.log('sending id');
            postWithoutAnswer('http://localhost:8000/api/v1/account/create_trainer/' + sending_data['id'] + '/', undefined, "POST", function () {location.href = '../html/federation_coaches.html'});
        }
    else if (checkInputsInSendingData(sending_data)) {
        console.log(sending_data);
        postWithoutAnswer('http://localhost:8000/api/v1/account/create_trainer/', JSON.stringify(sending_data), "POST", function () {location.href = '../html/federation_coaches.html'});
    }
    else {
        document.getElementById('error-message').classList.remove('hidden');
    }

}

function changeType(inputNode, type, defaultValue) {
    inputNode.type = type;
    if (defaultValue !== undefined)
        inputNode.placeholder = defaultValue;
}