function createCards() {
    let clubs = getClubInfo();
    for (let club of clubs) {
        let card = document.createElement('div');
        card.classList.add('card');
        card.classList.add('bordered-container');
        fillCard(card, club);

        let but = document.getElementsByClassName('add_club')[0];
        insertBefore(card, but);
    }
}

function fillCard(cardNode, clubInfo) {
    let html = '<div className="ro">' +
         '<img src="'+ clubInfo['logo'] +'">' +
           '<div class="inf-list">' +
               '<p class="club_name">'+ clubInfo['name'] +'</p>' +
               '<p class="city">г.' + clubInfo['city'] + '</p>' +
               '<p class="region">'+ clubInfo['area'] +'</p>';
    for (let trainer of clubInfo['main_trainers']) {
        html += '<p class="fio">'+ trainer +'</p>';
    }
    html += '</div>\n' +
        '</div>' +
        '<div class="po">\n' +
        '       <button type="button" class="deleteBut" name="delete">Удалить</button>\n' +
        '       <button type="button" class="editBut" name="edit">Редактировать</button>\n' +
        '   </div>'
    cardNode.innerHTML = html;
}

function insertBefore(newNode, existingNode) {
    existingNode.parentNode.insertBefore(newNode, existingNode);
}

function getClubInfo() {
    // return JSON.parse(getJsonFromServer(url));
    return [{"name": "Прайм", "city": "Екатеринбург", "area": "Свердловская область", "logo": "../assets/clubs_logo/Praim.png", "main_trainers": ["Некто Нектович Нектов", "Иванов Иван Иванович"]},
        {"name": "Практика", "city": "Екатеринбург", "area": "Свердловская область", "logo": "../assets/clubs_logo/Практика.png", "main_trainers": ["Некто Нектович Нектов", "Иванов Иван Иванович"]}];
}

createCards();