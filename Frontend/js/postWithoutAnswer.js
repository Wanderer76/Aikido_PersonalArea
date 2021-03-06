function postWithoutAnswer(url, sendingFile, method="POST", func, datatype = undefined) {
    let xhr = new XMLHttpRequest();
    let storage = window.sessionStorage;
    xhr.open(method, url);
    xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'));
    if (datatype == 'json')
        xhr.setRequestHeader('Content-type', 'application/json');
    if (sendingFile !== undefined)
        xhr.send(sendingFile);
    else
        xhr.send();


    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status >= 200 && this.status < 400) {
            console.log(xhr.response);
            func();
        }
    }
}