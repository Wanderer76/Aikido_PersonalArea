import {createElement, render, RenderPosition} from "./add-event-render-script.js";
import {dayInputs, hoursInputs, dayClickListener, dayChangeListener, addHiddenClass} from "./add-event-schedule-script.js";

export const eventSlug = sessionStorage.getItem('slug');
getRequest(`http://localhost:8000/api/v1/events/event_statistic/${eventSlug}/`, fillInputs);

function fillInputs(data) {
    let parsed = JSON.parse(data)['result'];
    console.log(parsed);

    document.getElementById('event-name').value = parsed['event_name'];
    document.getElementById('date-start').value = parsed['date_of_event'];
    document.getElementById('date-end').value = parsed['end_of_event'];
    document.getElementById('event-location').value = parsed['address'];
    document.getElementById('resp-club-select').value = parsed['responsible_club'];
    document.getElementById('lead-coach').value = parsed['responsible_trainer'];
    document.getElementById('max-rang-select').value = parsed['max_rang'];

    // не работает.
    document.getElementById('logo-icon-preview').src = parsed['logo_img'];
    document.getElementById('coach-icon-preview').src = parsed['couch_img'];
    document.getElementById('event-poster-preview').src = parsed['poster'];

    const coachOffset = parsed['coach_offset'];
    document.getElementById('coach-x-offset').value = coachOffset['x_offset'];
    document.getElementById('coach-y-offset').value = coachOffset['y_offset'];

    const logoOffset = parsed['logo_offset'];
    document.getElementById('logo-x-offset').value = logoOffset['x_offset'];
    document.getElementById('logo-y-offset').value = logoOffset['y_offset'];

    const contacts = parsed['contacts'];
    document.getElementById('org-name').value = contacts['org_name'];
    document.getElementById('org-phone').value = contacts['org_phone'];
    document.getElementById('org-email').value = contacts['org_email'];

    createSchedule(parsed['schedule']);
}

function createSchedule(schedule) {
    for (let category in schedule) {
        createCurrentCategorySchedule(category, schedule[category]);
    }

    dayClickListener();
    dayChangeListener();
    addHiddenClass(dayInputs);
    addHiddenClass(hoursInputs);
}

function createCurrentCategorySchedule (category, categorySchedule) {
    if (Object.keys(categorySchedule).length !== 0) {
        for (let day in categorySchedule) {
            createDay(category, day);
            createHours(category, day, categorySchedule[day]);
        }

    }
}

function createDay (category, day) {
    const markup = `<input type="text" class="input-schedule" data-category="${category}" placeholder="ДД месяц">`;
    const dayInputElement = createElement(markup);
    const dayColumn = document.getElementById('day-column');

    dayInputElement.value = day;
    dayInputs.push(dayInputElement);

    render(dayColumn, dayInputElement, RenderPosition.BEFOREEND);
}

function createHours (category, day, hours) {
    const markup = `<input type="text" class="input-schedule" data-day="${day}" data-category="${category}"  placeholder="ЧЧ:ММ - ЧЧ:ММ">`;
    const hoursColumn = document.getElementById('time-column');

    for (let i = 0; i < hours.length; i++) {
        const hoursInputElement = createElement(markup);
        hoursInputElement.value = hours[i];
        hoursInputs.push(hoursInputElement);

        render(hoursColumn, hoursInputElement, RenderPosition.BEFOREEND);
    }
}

