import {createElement, render, RenderPosition} from "./add-event-render-script.js";

// Разметка поля ввода в столбце дней.
const createDayInputMarkup = (dayCount, participantCategory) => {
    return `<input type="text" class="input-schedule" data-category="${participantCategory}" id="day-${dayCount}" placeholder="ДД месяц">`;
};

// Разметка поля ввода в столбце времени.
const createHoursInputMarkup = (hoursCount, exactDay, participantCategory) => {
    return `<input type="text" class="input-schedule" data-day="${exactDay}" 
        data-category="${participantCategory}" id="time-${hoursCount}" placeholder="ЧЧ:ММ - ЧЧ:ММ">`;
};

// Элементы.

const participantSelect = document.getElementById('participant-category');
const dayColumn = document.getElementById('day-column');
const hoursColumn = document.getElementById('time-column');
const addDayBtn = document.getElementById('add-day');
const addHoursBtn = document.getElementById('add-time');

// Счётчики элементов дней и времени.

let dayInputCount = 0;
let hoursInputCount = 0;

// Массивы для хранения элементов дней и времени.

let dayInputs = [];
let hoursInputs = [];

let currentDayElement = null;

//Обработчик клика для выбора категории участников.
participantSelect.addEventListener('change', function () {
    currentDayElement = null;
    addHiddenClass(dayInputs);
    addHiddenClass(hoursInputs);
    removeDayHiddenClass(dayInputs, participantSelect.value);
})

//Убирает класс, скрывающий элемент дня.
const removeDayHiddenClass = (days, category) => {
    for (let j = 0; j < days.length; j++) {
        if (days[j].dataset.category === category) {
            days[j].classList.remove('visually-hidden');
        }
    }
}

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

        removeCurrentDay();
        addHiddenClass(hoursInputs);

        dayInputCount++;

        console.log(dayInputElement);
    }
    else {
        alert('Выберите категорию.');
    }
}

// Функция, навешивающая слушателя на клик каждого элемента массива дней.
const dayClickListener = () => {
    for (let i = 0; i < dayInputs.length; i++) {
        dayInputs[i].addEventListener('click', function () {
            addHiddenClass(hoursInputs);
            removeCurrentDay();
            dayInputs[i].classList.add('chosen-schedule');
            currentDayElement = dayInputs[i];
            removeHoursHiddenClass(hoursInputs, currentDayElement.value, participantSelect.value);
        })
    }
}

// Убирает класс, скрывающий элемент часов
const removeHoursHiddenClass = (hours, chosenDay, category) => {
    for (let j = 0; j < hours.length; j++) {
        if (hours[j].dataset.day === chosenDay && hours[j].dataset.category === category) {
            hours[j].classList.remove('visually-hidden');
        }
    }
}

// Функция, навешивающая слушателя на изменение каждого элемента массива дней.
const dayChangeListener = () => {
    for (let i = 0; i < dayInputs.length; i++) {
        dayInputs[i].addEventListener('change', function () {
            let changedDay = dayInputs[i];
            changeDateData(hoursInputs, changedDay);
        })
    }
}

// Функция замены поля измененной даты у выбранных дней.
const changeDateData = (hours, changedDayInput) => {
    for (let j = 0; j < hours.length; j++) {
        if (!hours[j].classList.contains('visually-hidden') && hours[j].dataset.category === changedDayInput.dataset.category) {
            hours[j].dataset.day = changedDayInput.value;
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
addHoursBtn.addEventListener('click', function () { addHours(); })

const addHours = () => {
    if (currentDayElement) {
        const count = hoursInputCount;
        const exactDay = currentDayElement.value;
        const hoursInputElement = createElement(createHoursInputMarkup(count, exactDay, participantSelect.value));

        hoursInputs.push(hoursInputElement);
        render(hoursColumn, hoursInputElement, RenderPosition.BEFOREEND);
        hoursInputCount++;

        console.log(hoursInputElement, hoursInputCount);
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

//Функция формирования итогового расписания
export function createSchedule(days = dayInputs, hours = hoursInputs) {
    const categories = ["children-jun", "children-sen", "adults", "qualify"];
    let schedule = {};

    for (let i = 0; i < categories.length; i++) {
        createCurrentGroupSchedule(categories[i], schedule);
    }

    function createCurrentGroupSchedule (currentCategory, schedule) {
        let result = {};
        for (let i = 0; i < days.length; i++) {
            if (days[i].value && days[i].dataset.category === currentCategory) {
                result[days[i].value] = [];
                for (let j = 0; j < hours.length; j++) {
                    if (hours[j].value && hours[j].dataset.day === days[i].value && hours[j].dataset.category === currentCategory) {
                        result[days[i].value].push(hours[j].value);
                    }
                }
            }
        }
        Object.keys(result).forEach(function(key) {
            if (result[key].length === 0) {
                delete result[key];
            }
        }, result);
        schedule[currentCategory] = result;
    }
    //console.log(schedule);
    return(schedule);
}

