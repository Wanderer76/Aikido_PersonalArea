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



//Обработчик клика для кнопки "Добавить день".
addDayBtn.addEventListener('click', function (event) {
    removeCurrentDay();
    addDay();
    addDayClickListener();
})

// Функция создания и отрисовки элемента, добавления его в массив.
const addDay = () => {
    if (participantSelect.value.length > 0) {
        const count = dayInputCount;
        const category = participantSelect.value;
        const dayInputElement = createElement(createDayInputMarkup(count, category));

        dayInputs.push(dayInputElement);
        render(dayColumn, dayInputElement, RenderPosition.AFTERBEGIN);
        addHiddenClass();
        dayInputCount++;

        console.log(dayInputElement, dayInputCount);
    }
    else {
        alert('Выберите категорию');
    }
}

// Функция, навешивающая слушателя на каждый элемент массива.
const addDayClickListener = () => {
    for (let i = 0; i < dayInputs.length; i++) {
        dayInputs[i].addEventListener('click', function (event) {
            addHiddenClass();
            removeCurrentDay();
            dayInputs[i].classList.add('chosen-schedule');
            currentDayElement = dayInputs[i];
            removeHiddenClass();
        })
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
addTimeBtn.addEventListener('click', function (event) {
    addTime();

})

const addTime = () => {
    if (currentDayElement) {
        const count = timeInputCount;
        const exactDay = currentDayElement.value;
        const timeInputElement = createElement(createTimeInputMarkup(count, exactDay));

        timeInputs.push(timeInputElement);
        render(timeColumn, timeInputElement, RenderPosition.AFTERBEGIN);
        timeInputCount++;

        console.log(timeInputElement, timeInputCount);
    }
    else {
        alert('Выберите день');
    }
}

//Добавляет класс, скрывающий элемент
const addHiddenClass = () => {
    for (let j = 0; j < timeInputs.length; j++) {
        timeInputs[j].classList.add('visually-hidden');
    }
}

//Убирает класс, скрывающий элемент
const removeHiddenClass = () => {
    for (let j = 0; j < timeInputs.length; j++) {
        if (timeInputs[j].name === currentDayElement.value) {
            timeInputs[j].classList.remove('visually-hidden');
        }
    }
}
