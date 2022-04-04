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
    return `<input type="text" class="input-schedule" name="${participantCategory}" id="day-${dayCount}">`;
};

// Разметка поля ввода в столбце времени.
const createTimeInputMarkup = () => {
    return `<input type="text" class="input-schedule">`;
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

let currentDayInput = null;



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
            removeCurrentDay();
            dayInputs[i].classList.add('chosen-schedule');
            currentDayInput = dayInputs[i];
        })
    }
}

// Функция обнуления выбранного дня.
const removeCurrentDay = () => {
    for (let j = 0; j < dayInputs.length; j++) {
        dayInputs[j].classList.remove('chosen-schedule');
    }
    currentDayInput = null;
}

//Обработчик для кнопки "+" время.
addTimeBtn.addEventListener('click', function (event) {
    let timeInputElement = createElement(createTimeInputMarkup());
    render(timeColumn, timeInputElement, RenderPosition.AFTERBEGIN);
})
