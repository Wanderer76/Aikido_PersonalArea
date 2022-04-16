let xhr = new XMLHttpRequest();
let storage = window.sessionStorage;
let url = 'http://localhost:8000/api/v1/account/profile/';

xhr.open('GET', url);
xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'))
xhr.send();

xhr.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        let data = xhr.response;
        setOutputParams(data);
    }
}

function setOutputParams(jsonData) {
    jsonData = JSON.parse(jsonData);
    setBaseInfo(jsonData);
    setAchievmentStory(jsonData);
    setAchievmentStoryInTable(jsonData);
    setBelt(jsonData);
}

function setBelt(data) {
    console.log(data);
    let belt = getBeltColor(data.seminars);
    console.log(belt);
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
    for (var i = 0; i < data.seminars.length; i++) {
        displayAchievment(data.seminars[i]);
    }
}

function displayAchievment(achievment) {
    let id = getAchievmentBlockId(achievment);
    if (id == null)
        return;
    let num = id.substring(0, 1);
    let name = id.substring(1, id.length);
    for (var i = num; i < 6; i++) {
        let block = document.getElementById(i + name);
        block.classList.remove('not-reached');
        if (i == num) {
            block.children[1].children[0].textContent = achievment.name;
            block.children[1].children[1].textContent = setDateFormat(achievment.attestation_date);
        }
    }
}

function getAchievmentBlockId(achievment) {
    let id;
    if (achievment.isChild) {
        if (achievment.newKu > 10) {
            console.log("Error achievment: dan was assigned to child");
            return;
        }
        if (achievment.newKu < 0 || achievment.newKu > 5) {
            console.log("Uncorrect degree: " + achievment.newKu + 'was');
            return;
        }
        else
            id = achievment.newKu + 'ku-child';
    }

    else {
        if (achievment.newKu > 10)
            id = achievment.newKu % 10 + 'dan';
        else {
            if (achievment.newKu < 0 || achievment.newKu > 5) {
                console.log("Uncorrect degree: " + achievment.newKu + 'was');
                return;
            }
            else
                id = achievment.newKu + 'ku';
        }
    }
    return id;
}


function setAchievmentStoryInTable(data) {
    let header = document.getElementById('seminar-header');
    for (var i = 0; i < data.seminars.length; i++) {
        let output = document.createElement('tr');

        result = data.seminars[i].newKu == data.seminars[i].oldKu ? 0 : data.seminars[i].newKu;
        if (result > 10) {
            result = result % 10 + ' дан';
        } else {
            result = result + ' кю';
        }

        output.innerHTML =
            '<td>' + setDateFormat(data.seminars[i].attestation_date) + '</td>' +
            '<td class="unvisible bordered">' + data.seminars[i].city + '</td>' +
            '<td class="unvisible bordered">' + data.seminars[i].club + '</td>' +
            '<td>' + result + '</td>';
        header.parentElement.insertBefore(output, header.nextSibling);
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


function fillBar(progress) {
    progress.style.width = progress.getAttribute('data-done') + '%';
    progress.style.opacity = 1;
}

function changeBarColor(progressBar, color) {
    progressBar.style.background = color;
}

function showBlock(button, block, textValue) {
    if (button.textContent === textValue +  ' ▼')
        button.textContent = textValue + ' ▲';
    else
        button.textContent = textValue + ' ▼';
    block.classList.toggle('visually-hidden');

}

fillBar(document.getElementsByClassName('progress-done')[0]);
changeBarColor(document.getElementsByClassName('progress-done')[0], '#0417b4');
fillBar(document.getElementsByClassName('progress-done')[1]);
changeBarColor(document.getElementsByClassName('progress-done')[1], '#9e4700');

