setStatusAbility();

function setStatusAbility() {
    let adminButton = document.getElementById("admin-button");
    let trainerButton = document.getElementById("trainer-button");
    if (window.sessionStorage.getItem('status') == 'trainer')
        adminButton.classList.add("hidden");
    else if (window.sessionStorage.getItem('status') == 'user') {
        adminButton.classList.add('hidden');
        trainerButton.classList.add('hidden');
    }

}