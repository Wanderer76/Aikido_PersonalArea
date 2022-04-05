function postWithoutAnswer(url, sendingFile, method="POST", func) {
    let xhr = new XMLHttpRequest();
    let storage = window.sessionStorage;
    xhr.open(method, url);
    xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'));
    if (sendingFile !== undefined)
        xhr.send(sendingFile);
    else
        xhr.send();

    func();


    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status > 200 && this.status < 400) {
            console.log(xhr.response);
            func();
        }
    }
}