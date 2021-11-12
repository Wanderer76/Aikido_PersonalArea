const url = "http://localhost:8000/api/v1/account/login/";

let butt = document.querySelector(".enter-button");
let id;
let pass;
let xhr = new XMLHttpRequest();
xhr.responseType = 'json';
let token;

butt.onclick = function () {
    id = document.getElementById('id').value;
    pass = document.getElementById('pass').value;

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            token = xhr.response;
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