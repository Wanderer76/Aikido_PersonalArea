const url = "http://localhost:8000/api/v1/account/login/";

let butt = document.querySelector(".enter-button");
let errorMessage = document.querySelector('.error-message');
let idForm = document.getElementById('id');
let passForm = document.getElementById('pass');
let id;
let pass;
let xhr = new XMLHttpRequest();
xhr.responseType = 'json';

let storage = window.sessionStorage;
xhr.onreadystatechange = function () {
    // if (this.readyState == 4 && this.status == 200) {
    //     console.log(xhr.response);
    //     checkToken(xhr.response);
    // }
    console.log(xhr.response);
    checkToken(xhr.response);
};

butt.onclick = function () {
    id = idForm.value;
    pass = passForm.value;
    xhr.open("POST", url);

    let json = JSON.stringify({
            "id": parseInt(id),
            "password": pass.toString()
        });
    xhr.send(json);
}

idForm.onchange = function () {
    errorMessage.classList.add('hide');
}

passForm.onchange = function () {
    errorMessage.classList.add('hide')
}

function checkToken(info) {
    if ("token" in info){
        storage.setItem('user_token', info.token);
        storage.setItem('status', info.status);
        location.href = "../html/profile.html";
    } else {
        errorMessage.classList.remove('hide');
        console.log("Неправильный логин-пароль");
    }
}