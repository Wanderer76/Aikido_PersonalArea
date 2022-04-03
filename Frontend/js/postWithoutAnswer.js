function postWithoutAnswer(url, sendingFile) {
    let xhr = new XMLHttpRequest();
    let storage = window.sessionStorage;
    xhr.open("POST", url);
    xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'));
    xhr.send(sendingFile);


    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(xhr.response);
        }
    }
}