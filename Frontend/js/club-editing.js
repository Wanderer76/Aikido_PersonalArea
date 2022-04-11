getRequest('http://localhost:8000/api/v1/clubs/get_club/' + window.sessionStorage.getItem('club_slug') + '/', fillInputs);

function fillInputs(data) {
    let parsed = JSON.parse(data)
    console.log(parsed)
    document.getElementById('club-name').value = parsed['name'];
    document.getElementById('area').value = parsed['area'];
    document.getElementById('city').value = parsed['city'];
    document.getElementById('logo-icon-preview').src = parsed['logo'];
    for (let coach of parsed['main_trainers']) {
        addMoreCoach(coach['id']);
    }
}

function sendUpdatedInfo() {
    let url = 'http://localhost:8000/api/v1/clubs/update_club/' + window.sessionStorage.getItem('club_slug') + '/';
    sendAllInfo(url, "PATCH");
}