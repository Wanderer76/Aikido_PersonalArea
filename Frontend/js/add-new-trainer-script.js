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
    let selector = document.getElementById('club-selector');
    for (let club of clubs) {
        selector.innerHTML += '<option value="'+ club['name'] + '">'+ club['name'] +'</option>';
    }
}

fillClubSelector(JSON.stringify([{'name' : "Something club name1", 'logo': 'dsvndufvbid'}, {'name' : "Something club name2", 'logo': 'dsvndufvbid'}]))
fillTrainerSelector(JSON.stringify([{'id' : '001', 'name': "Некто Нектович Нектов"}, {'id' : '002', 'name': "Башмачкин Акакий Акакиевич"}]));


function getAllInfo() {

    if (document.getElementById('coach-selector').value !== 'none') {
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

function sendInfo() {
    let sending_data = getAllInfo();
    if (sending_data['id'] !== 'none' && sending_data['id'] !== undefined) {
            console.log('sending id');
            postWithoutAnswer('http://localhost:8000/api/v1/account/create_trainer/' + sending_data['id'] + '/', undefined, "POST", function () {location.href = '../html/federation_coaches.html'});
        }
    else if  (sending_data['surname'] !== '' && sending_data['name'] !== '' && sending_data['second_name'] !== '' &&
        sending_data['birthdate'] !== '' && sending_data['rank'] !== 'none' && sending_data['club'] !== 'none' &&
        sending_data['last_event'] !== '') {
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