const url = "http://localhost:8000/api/v1/account/login/";

// let loginInput = document.querySelector("#id");
// let passInput = document.querySelector("#pass");
let butt = document.querySelector(".enter-button");
let id = 1345;
let pass = "qwerty1234";

butt.onclick = function () {
    id = document.getElementById('id').value;
    pass = document.getElementById('pass').value;

    let xhr = new XMLHttpRequest();
    xhr.responseType = 'json';

    let json = {"id": id,
        "password": pass};

    let token = "";
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            token = xhr.response.message;
        }
    };
    console.log(json);
    xhr.open("POST", url, true);
    xhr.send(json);

}




