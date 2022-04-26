getRequest('http://localhost:8000/api/v1/account/profile/', setOutputParams);

let storage = window.sessionStorage;

function setOutputParams(jsonData) {
    console.log(jsonData);
    jsonData = JSON.parse(jsonData);
    setBaseInfo(jsonData);
    setAchievmentStory(jsonData);
    setAchievmentStoryInTable(jsonData.seminars, document.getElementById('seminar-header'));
    setFutureEvents(jsonData.events, document.getElementById('future-seminar-header'))
    setBelt(jsonData);
    fillAchievmentCard('.card[name="card-received"]', jsonData);
    fillAchievmentCard('.card[name="card-next"]', jsonData, false);
}

function fillAchievmentCard(cardNodeSelector, data, received=true,) {
    let eventNameNode = document.querySelector(cardNodeSelector + '> p[name="event-name"]');
    if (eventNameNode !== null)
        eventNameNode.textContent = data.seminar_name;
    document.querySelector(cardNodeSelector + '> p[name="event-date"]').textContent = received ? setDateFormat(data.seminar_date) : setDateFormat(data.next_seminar_date);

    let progressBar = document.querySelector(cardNodeSelector + '>.prog>.progress-done');
    fillBar(progressBar, received, data.seminar_date, data.next_seminar_date);
    changeBarNameAndColor(progressBar, received ? data.received_ku : data.next_ku);

}

function fillBar(progress, full = true, startStrDate, endStrDate) {
    if (!full) {
        let startDate = new Date(startStrDate);
        let endDate = new Date(endStrDate);
        let now = Date.now();
        let dif = (endDate - now) / (endDate - startDate) * 100;
        progress.dataset.done = dif >= 100 || dif < 0 ? 100 : Math.round(dif);
    } else {
        progress.dataset.done = 100;
    }
    progress.style.width = progress.getAttribute('data-done') + '%';
    progress.style.opacity = 1;
}

function changeBarNameAndColor(progressBar, ku) {
    let className;
    if (ku > 10) {
        className = 'dan';
        progressBar.textContent = ku % 10 === 0 ? 10 + ' дан' : ku % 10 + ' дан';
    } else {
        className = 'ku-'+ku;
        progressBar.textContent = ku + ' кю';
    }
    progressBar.classList.add(className);
}

function setBelt(data) {
    console.log(data);
    let belt = getBeltColor(data.seminars);
    document.getElementById('belt-img').src = '../assets/belts/'+ belt +'_belt.jpg';
}

function getBeltColor(seminars, isChild) {
    if (seminars.length == 0 || seminars == null)
        return 'white';
    let maxChildAchievment = getMaxKu(seminars, isChild);
    let maxAchievment = getMaxKu(seminars, isChild);
    if (maxAchievment == 6)
        maxAchievment = maxChildAchievment;
    switch (maxAchievment) {
        case 5:
            return 'yellow';
        case 4:
            return 'red';
        case 3:
            return 'green';
        case 2:
            return 'blue';
        case 1:
            return 'brown';
        default:
            return 'black';
    }
}

function getMaxKu(seminars, isChild) {
    let maxAchievment = 6;
    for (let i = 0; i< seminars.length; i++){
        if (isChild == seminars[i].isCHild)
            if ((seminars[i].newKu > 10 && seminars[i].newKu > maxAchievment) || (seminars[i].newKu < maxAchievment && maxAchievment < 10))
                maxAchievment = seminars[i].newKu;
    }
    return maxAchievment;
}

function setAchievmentStory(data) {
    for (let i = 0; i < data.seminars.length; i++) {
        displayAchievment(data.seminars[i]);
    }
}

function displayAchievment(achievment) {
    let id = achievment.is_child ? achievment.received_ku + '-child' : achievment.received_ku;
    console.log(id);
    if (id == null)
        return;
    let block = document.getElementById(id);
    block.classList.remove('visually-hidden');
    block.classList.remove('not-reached');
    console.log(achievment.event_name);
    block.children[1].children[0].textContent = achievment.event_name;
    block.children[1].children[1].textContent = setDateFormat(achievment.attestation_date);
}


function setAchievmentStoryInTable(events, tableHeader) {
    console.log(events);
    for (var i = 0; i < events.length; i++) {
        let output = document.createElement('tr');

        let result = events[i].received_ku;
        if (result > 10) {
            result = result % 10 + ' дан';
        } else if (result < 6) {
            result = result + ' кю';
        }

        output.innerHTML =
            '<td>' + setDateFormat(events[i].attestation_date) + '</td>' +
            '<td class="unvisible bordered">' + events[i].event_name + '</td>' +
            '<td class="unvisible bordered">' + events[i].address + '</td>' +
            '<td>' + result + '</td>';
        tableHeader.parentElement.insertBefore(output, tableHeader.nextSibling);
    }
}

function setFutureEvents(events, tableHeader) {
    console.log(events);
    for (var i = 0; i < events.length; i++) {
        let output = document.createElement('tr');

        let result = events[i].received_ku;
        if (result > 10) {
            result = result % 10 + ' дан';
        } else if (result < 6) {
            result = result + ' кю';
        }

        output.innerHTML =
            '<td>' + createDateOutput(events[i].date_of_event, events[i].end_of_event) + '</td>' +
            '<td class="unvisible bordered">' + events[i].event_name + '</td>' +
            '<td class="unvisible bordered">' + events[i].address + '</td>' +
            '<td><button type="button" name="apple" class="apply">Подробнее</button></td>';
        tableHeader.parentElement.insertBefore(output, tableHeader.nextSibling);
    }
}

function setBaseInfo(data) {
    document.getElementById('name').textContent = data.name;
    document.getElementById('surname').textContent = data.surname;
    document.getElementById('birthdate').textContent = setDateFormat(data.birthdate);
    document.getElementById('id-button').textContent = 'ID #' + data.id;
    storage.setItem('myId', data.id);
    if (data.photo !== null)
        document.getElementById('photo').src = data.photo;
    if (data.club == null || data.club == 'null')
        console.log('null photo');
    else {
        document.getElementById('club-photo').src = '../assets/clubs_logo/'+ data.club + '.png';
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


function showBlock(button, block, textValue) {
    if (button.textContent === textValue +  ' ▼')
        button.textContent = textValue + ' ▲';
    else
        button.textContent = textValue + ' ▼';
    block.classList.toggle('visually-hidden');
}

function createDateOutput(date1, date2) {
    var startDate = new Date(date1);
    var endDate = new Date(date2);
    if (startDate.getMonth() == endDate.getMonth() && startDate.getFullYear() == endDate.getFullYear())
        return startDate.getDate() + " - " + endDate.getDate() + " " + endDate.toLocaleString('default', {month: 'long'}) + " "+ endDate.getFullYear();
    else if (startDate.getMonth() !== endDate.getMonth() && startDate.getFullYear() == endDate.getFullYear())
        return startDate.getDate() + " " + startDate.toLocaleString('default', {month: 'long'}) + " - " +
            endDate.getDate() + " " + endDate.toLocaleString('default', {month: 'long'}) + " " + startDate.getFullYear();
    else return startDate.getDate() + " " +startDate.toLocaleString('default', {month: 'long'}) + " " + startDate.getFullYear() + " - " +
            endDate.getDate() + " " + endDate.toLocaleString('default', {month: 'long'}) + " " + endDate.getFullYear();
}



