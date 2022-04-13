getRequest('http://localhost:8000/api/v1/events/event_statistic/sorevnovanie-11/', fillInputs);

function fillInputs(data) {
    let parsed = JSON.parse(data)
    console.log(parsed)

    document.getElementById('event-name').value = parsed['event_name'];
    document.getElementById('date-start').value = parsed['date_of_event'];
    document.getElementById('date-end').value = parsed['end_of_event'];
    document.getElementById('event-location').value = parsed['address'];
    document.getElementById('resp-club-select').value = parsed['responsible_club'];
    document.getElementById('lead-coach').value = parsed['responsible_trainer'];
    document.getElementById('max-rang-select').value = parsed['max_rang'];

    // let couchImage = document.getElementById('coach-icon');
    // let couchXOffset = document.getElementById('coach-x-offset');
    // let couchYOffset = document.getElementById('coach-y-offset');
    //
    // let logoImage = document.getElementById('logo-icon');
    // let logoXOffset = document.getElementById('logo-x-offset');
    // let logoYOffset = document.getElementById('logo-y-offset');
    //
    // let posterImage = document.getElementById('event-poster');
    //
    // let orgName = document.getElementById('org-name');
    // let orgPhone = document.getElementById('org-phone');
    // let orgEmail = document.getElementById('org-email');

}

// function sendUpdatedInfo() {
//     let url = 'http://localhost:8000/api/v1/clubs/update_club/' + window.sessionStorage.getItem('club_slug') + '/';
//     sendAllInfo(url, "PATCH");
// }