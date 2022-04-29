import {createElement, render, RenderPosition} from "./add-event-render-script.js";

getRequest('http://localhost:8000/api/v1/clubs/get_clubs/', createClubsSelect);

function createClubsSelect(data) {
    let parsed = JSON.parse(data);

    function createClubsOffsetMarkup(item) {
        const inputElement = createElement(`<option class="resp-club-opt" value="${item.name}">${item.name}</option>`);
        const clubsSelect = document.getElementById('resp-club-select');
        render(clubsSelect, inputElement, RenderPosition.BEFOREEND);
    }

    parsed.forEach(createClubsOffsetMarkup);
}
