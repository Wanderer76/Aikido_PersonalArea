const url = "http://localhost:8000/api/v1/account/login/";

let id = 1345;
let pass = "qwerty1234";

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
xhr.open("POST", url, true);
xhr.send(json);



