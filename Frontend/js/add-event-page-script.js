// Рендеринг.
const RenderPosition = {
    BEFOREBEGIN: 'beforebegin',
    AFTERBEGIN: 'afterbegin',
    BEFOREEND: 'beforeend',
    AFTEREND: 'afterend',
};

const render = (container, element, place) => {
    switch (place) {
        case RenderPosition.BEFOREBEGIN:
            container.before(element);
            break;
        case RenderPosition.AFTERBEGIN:
            container.prepend(element);
            break;
        case RenderPosition.BEFOREEND:
            container.append(element);
            break;
        case RenderPosition.AFTEREND:
            container.after(element);
            break;
    }
};

const createElement = (template) => {
    const newElement = document.createElement('div');
    newElement.innerHTML = template;

    return newElement.firstChild;
};

// Разметка поля ввода в столбце дней.
const createDayInputMarkup = (dayCount, participantCategory) => {
    return `<input type="text" class="input-schedule" name="${participantCategory}" id="day-${dayCount}" placeholder="ДД месяц">`;
};

// Разметка поля ввода в столбце времени.
const createTimeInputMarkup = (timeCount, exactDay) => {
    return `<input type="text" class="input-schedule" name="${exactDay}" id="time-${timeCount}" placeholder="ЧЧ:ММ - ЧЧ:ММ">`;
};

// Элементы.
const participantSelect = document.getElementById('participant-category');
const dayColumn = document.getElementById('day-column');
const timeColumn = document.getElementById('time-column');
const addDayBtn = document.getElementById('add-day');
const addTimeBtn = document.getElementById('add-time');

// Счётчики элементов дней и времени.

let dayInputCount = 0;
let timeInputCount = 0;

// Массивы для хранения элементов дней и времени.


let dayInputs = [];
let timeInputs = [];

let currentDayElement = null;

//Обработчик клика для выбора категории участников.
participantSelect.addEventListener('change', function () {
    currentDayElement = null;
    addHiddenClass(dayInputs);
    addHiddenClass(timeInputs);
    removeHiddenClass(dayInputs, participantSelect.value);
})


//Обработчик клика для кнопки "Добавить день".
addDayBtn.addEventListener('click', function () {
    removeCurrentDay();
    addDay();
    dayClickListener();
    dayChangeListener();
})

// Функция создания и отрисовки элемента, добавления его в массив.
const addDay = () => {
    if (participantSelect.value.length > 0) {
        const count = dayInputCount;
        const category = participantSelect.value;
        const dayInputElement = createElement(createDayInputMarkup(count, category));

        dayInputs.push(dayInputElement);
        render(dayColumn, dayInputElement, RenderPosition.BEFOREEND);
        addHiddenClass(timeInputs);
        dayInputCount++;

        console.log(dayInputElement, dayInputCount);
    }
    else {
        alert('Выберите категорию');
    }
}

// Функция, навешивающая слушателя на клик каждого элемента массива дней.
const dayClickListener = () => {
    for (let i = 0; i < dayInputs.length; i++) {
        dayInputs[i].addEventListener('click', function () {
            addHiddenClass(timeInputs);
            removeCurrentDay();
            dayInputs[i].classList.add('chosen-schedule');
            currentDayElement = dayInputs[i];
            removeHiddenClass(timeInputs, currentDayElement.value);
        })
    }
}

// Функция, навешивающая слушателя на изменение каждого элемента массива дней.
const dayChangeListener = () => {
    for (let i = 0; i < dayInputs.length; i++) {
        dayInputs[i].addEventListener('change', function () {
            let changedDay = dayInputs[i];
            changeDateData(timeInputs, changedDay.value);
        })
    }
}

// Функция замены поля измененной даты у выбранных дней.
const changeDateData = (times, day) => {
    for (let j = 0; j < times.length; j++) {
        if (!times[j].classList.contains('visually-hidden')) {
            times[j].name = day;
        }
    }
}

// Функция обнуления выбранного дня.
const removeCurrentDay = () => {
    for (let j = 0; j < dayInputs.length; j++) {
        dayInputs[j].classList.remove('chosen-schedule');
    }
    currentDayElement = null;
}

//Обработчик для кнопки "+" время.
addTimeBtn.addEventListener('click', function () {
    addTime();

})

const addTime = () => {
    if (currentDayElement) {
        const count = timeInputCount;
        const exactDay = currentDayElement.value;
        const timeInputElement = createElement(createTimeInputMarkup(count, exactDay));

        timeInputs.push(timeInputElement);
        render(timeColumn, timeInputElement, RenderPosition.BEFOREEND);
        timeInputCount++;

        console.log(timeInputElement, timeInputCount);
    }
    else {
        alert('Выберите день');
    }
}

//Добавляет класс, скрывающий элемент
const addHiddenClass = (array) => {
    for (let j = 0; j < array.length; j++) {
            array[j].classList.add('visually-hidden');
        }
}

//Убирает класс, скрывающий элемент
const removeHiddenClass = (array, comparison) => {
    for (let j = 0; j < array.length; j++) {
        if (array[j].name === comparison) {
            array[j].classList.remove('visually-hidden');
        }
    }
}

//Функция формирования расписания
function createSchedule(days = dayInputs, times = timeInputs) {
    const categories = ["children-jun", "children-sen", "adults", "qualify"];
    let schedule = {};

    for (let i = 0; i < categories.length; i++) {
        createCurrentGroupSchedule(categories[i], schedule);
    }

    function createCurrentGroupSchedule (currentGroup, schedule) {
        let result = {};
        for (let i = 0; i < days.length; i++) {
            if (days[i].value && days[i].name === currentGroup){
                result[days[i].value] = [];
                for (let j = 0; j < times.length; j++) {
                    if (times[j].name === days[i].value && times[j].value) {
                        result[days[i].value].push(times[j].value);
                    }
                }
            }
        }
        Object.keys(result).forEach(function(key) {
            if (result[key].length === 0) {
                delete result[key];
            }
        }, result);
        schedule[currentGroup] = result;
    }
    console.log(schedule);
    return(schedule);
}

// Скрипт для формы загрузки
const inputLogo = document.getElementById('logo-icon');
const previewLogo = document.getElementById('logo-icon-preview');
inputLogo.addEventListener('change', function () {
    if (this.files &&
        this.files.length) {
        previewLogo.src = window.URL.createObjectURL(this.files[0]);
        previewLogo.setAttribute('height', '100%');
    } else {
        previewLogo.setAttribute('height', '100%');
        previewLogo.src = "../assets/empty-club-icon.png";
    }
});

const inputCoach = document.getElementById('coach-icon');
const previewCoach = document.getElementById('coach-icon-preview');
inputCoach.addEventListener('change', function () {
    if (this.files &&
        this.files.length) {
        previewCoach.src = window.URL.createObjectURL(this.files[0]);
        previewCoach.setAttribute('height', '100%');
    } else {
        previewCoach.setAttribute('height', '100%');
        previewCoach.src = "../assets/empty-coach-icon.png";
    }
});

const inputPoster = document.getElementById('event-poster');
const previewPoster = document.getElementById('event-poster-preview');
inputPoster.addEventListener('change', function() {
    if (this.files &&
        this.files.length) {
        previewPoster.src = window.URL.createObjectURL(this.files[0]);
        previewPoster.setAttribute('height', '100%');
    } else {
        previewPoster.setAttribute('height', '100px');
        previewPoster.src = "../assets/empty-poster.png";
    }
});

// Яндекс Карты
let coordinates = null;

function initMap() {
    let myMap = new ymaps.Map('map', {
        center: [56.838048312714704,60.60364972721357],
        zoom: 16,
        controls: []
    });

    let searchControl = new ymaps.control.SearchControl({
        options: {
            provider: 'yandex#map',
            noPlacemark: true
        }
    });

    searchControl.events.add('resultselect', function(e) {
        var index = e.get('index');
        searchControl.getResult(index).then(function(res) {

            coordinates = res.geometry.getCoordinates();
            myMap.geoObjects.removeAll();

            let placemark = new ymaps.Placemark(coordinates, {}, {});
            myMap.geoObjects.add(placemark);
        });
    })

    myMap.controls.add(searchControl);

    let eventLocation = document.getElementById('event-location');
    eventLocation.addEventListener('change', function() {
        update();
    })

    function update() {
        if (eventLocation.value) {
            searchControl.search(eventLocation.value);
        } else {
            myMap.geoObjects.removeAll();
            myMap.setCenter([56.838048312714704,60.60364972721357]);
            coordinates = null;
        }
    }
}

ymaps.ready(initMap);

//formData
let createButton = document.getElementById('create');

let eventTitle = document.getElementById('event-name');
let dateStart = document.getElementById('date-start');
let dateEnd = document.getElementById('date-end');
let locationField = document.getElementById('event-location');
let respClub = document.getElementById('resp-club-select');
let leadCoach = document.getElementById('lead-coach');
let maxRang = document.getElementById('max-rang-select');

let couchImage = document.getElementById('coach-icon');
let couchXOffset = document.getElementById('coach-x-offset');
let couchYOffset = document.getElementById('coach-y-offset');

let logoImage = document.getElementById('logo-icon');
let logoXOffset = document.getElementById('logo-x-offset');
let logoYOffset = document.getElementById('logo-y-offset');

let posterImage = document.getElementById('event-poster');

let orgName = document.getElementById('org-name');
let orgPhone = document.getElementById('org-phone');
let orgEmail = document.getElementById('org-email');

let couchImg = {
    x_offset: couchXOffset.value,
    y_offset: couchYOffset.value
}
const couchOffset = JSON.stringify(couchImg, null);

let logoImg = {
    x_offset: logoXOffset.value,
    y_offset: logoYOffset.value
}
const logoOffset = JSON.stringify(logoImg, null);

let contact = {
    org_name: orgName.value,
    org_phone: orgPhone.value,
    org_email: orgEmail.value
};
const contacts = JSON.stringify(contact, null);

const url = "http://127.0.0.1:8000/api/v1/events/create/";
let xhr = new XMLHttpRequest();
xhr.responseType = 'json';
let storage = window.sessionStorage;
let token = storage.getItem('user_token');

xhr.onreadystatechange = function () {
    let data = xhr.response;
    console.log(data);
    //location.href = '../html/admin-page-main.html';
};

let poster = new File([""], "../assets/empty-poster.png")

createButton.onclick = function () {

    xhr.open('POST', url);

    let formData = new FormData();

    let schedule = JSON.stringify(createSchedule(), null);

    formData.append("event_name", eventTitle.value);
    formData.append("date_of_event", dateStart.value);
    formData.append("end_of_event", dateEnd.value);
    formData.append("address", locationField.value);
    formData.append("coordinates", coordinates);
    formData.append("responsible_club", respClub.value);
    formData.append("responsible_trainer", leadCoach.value);
    formData.append("max_rang", maxRang.value);
    formData.append("schedule", schedule);
    formData.append("couch_img", couchImage.files[0]);
    formData.append("coach_offset", couchOffset);
    formData.append("logo_img", logoImage.files[0]);
    formData.append("logo_offset", logoOffset);
    formData.append("poster", posterImage.files[0]);
    formData.append("contacts", contacts);

    console.log(formData);
    xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'));
    xhr.send(formData);
}

