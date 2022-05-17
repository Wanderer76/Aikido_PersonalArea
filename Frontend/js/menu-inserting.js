let menu_inserting_element = document.createElement('div');
menu_inserting_element.classList.add('menu');
menu_inserting_element.innerHTML =
    '          <a href="#" class="menu-btn"></a>\n' +
    '          <nav class="container menu-list">\n' +
    '            <div class="btn">\n' +
    '                <div class="description"><a href="profile.html" class="text-a">Мой профиль</a></div>\n' +
    '                <div class="icon"><a href="profile.html"><img src="../assets/home.png"></a></div>\n' +
    '            </div>\n' +
    '            <div class="btn">\n' +
    '                <div class="description"><a href="../html/upcoming_events.html" class="text-a">Мероприятия</a></div>\n' +
    '                <div class="icon"><a href="../html/upcoming_events.html"><img src="../assets/competition.png"></a></div>\n' +
    '            </div>\n' +
    '            <div class="btn" id="trainer-button">\n' +
    '                <div class="description"><a href="service_page.html" class="text-a">Служебная</a></div>\n' +
    '                <div class="icon"><a href="service_page.html"><img src="../assets/service.png"></a></div>\n' +
    '            </div>\n' +
    '            <div class="btn" id="admin-button">\n' +
    '                <div class="description"><a href="admin-page-main.html" class="text-a">Админка</a></div>\n' +
    '                <div class="icon"><a href="admin-main-page.html"><img src="../assets/admin-icon.png"></a></div>\n' +
    '            </div>\n' +
    '            <div class="btn" id="edit-button">\n' +
    '                <div class="description"><a href="admin-page-main.html" class="text-a">Редактировать</a></div>\n' +
    '                <div class="icon"><a href="http://localhost:8000/admin/" target="_blank"><img src="../assets/edit.png"></a></div>\n' +
    '            </div>\n' +
    '            <img id="logo" src="../assets/logo_federation.png" alt="LOGO">\n' +
    '            <div class="exit-btn">\n' +
    '                <div class="description"><a href="authorization.html" class="text-a">Выйти</a></div>\n' +
    '                <div class="icon"><a href="authorization.html"><img src="../assets/exit-icon.png"></a></div>\n' +
    '            </div>\n' +
    '          </nav>';

let swipe_scrip = document.createElement("script");
swipe_scrip.src = "../js/navbar-swipe.js";
let set_status_ability_script = document.createElement("script");
set_status_ability_script.src = "../js/navbar-swipe.js";

function insert_last(element, insertingElementSelector) {
    let inserting_after_element = document.querySelector(insertingElementSelector);
    inserting_after_element.appendChild(element);
}

function insertElementBefore(element, insertingElementSelector) {
    let insertingElement = document.querySelector(insertingElementSelector);
    insertingElement.before(element);
}

function insert_link(rel, href) {
    let link = document.createElement("link");
    link.rel = rel;
    link.href = href;
    insert_last(link, "head");
}


insert_link("stylesheet", "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css");
insert_link("stylesheet", "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js");
insert_link("stylesheet", "../css/menu-style.css");
insertElementBefore(menu_inserting_element, ".content");
insert_last(swipe_scrip, "html");
insert_last(set_status_ability_script, "html");





