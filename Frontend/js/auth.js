const url = "http://localhost:8000/api/v1/account/login/";

let butt = document.querySelector(".enter-button");
let errorMessage = document.querySelector('.error-message');
let idForm = document.getElementById('id');
let passForm = document.getElementById('pass');
let id;
let pass;
let xhr = new XMLHttpRequest();
xhr.responseType = 'json';
let token;

butt.onclick = function () {
    id = idForm.value;
    pass = passForm.value;

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            token = xhr.response;
            if (checkToken(token)){
                errorMessage.classList.remove('hide');
            }
        }
        console.log(xhr.response)
    };

    let json = JSON.stringify({
        "id": parseInt(id),
        "password": pass.toString()
    });

    console.log(json);
    xhr.open("POST", url, true);
    xhr.send(json);
}

idForm.onchange = function () {
    errorMessage.classList.add('hide');
}

passForm.onchange = function () {
    errorMessage.classList.add('hide')
}

function checkToken(token) {
    return token.includes("error");
}