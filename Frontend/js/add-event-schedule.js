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
function createSchedule(days, times) {
    let result = {};
    for (let i = 0; i < days.length; i++) {
        if (days[i].value) {
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
    console.log(result);
}

let crtButton = document.getElementById('create');

crtButton.onclick = function() {createSchedule(dayInputs,  timeInputs)};
