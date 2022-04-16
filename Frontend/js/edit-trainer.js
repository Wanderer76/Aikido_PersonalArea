function hideAcceptBlock() {
    let acceptBlock = document.getElementById('accept-block');
    acceptBlock.classList.add('hidden');
}

function deleteCoach() {
    let id = sessionStorage.getItem('trainer_id');
    let acceptBlock = document.getElementById('accept-block');
    acceptBlock.classList.remove('hidden');
    let acceptBut = document.getElementsByClassName('accept-button')[0];
    acceptBut.onclick = function () {
        // postWithoutAnswer('http://localhost:8000/api/v1/clubs/delete_club/'+slug+'/', undefined, "DELETE", function () {location.reload()});
        console.log('Тренер должен удалиться');
    }
}