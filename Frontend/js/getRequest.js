function getRequest(url, func, method="GET") {
    let xhr = new XMLHttpRequest();
    let storage = window.sessionStorage;
    xhr.open(method, url);
    xhr.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'));
    xhr.send();
    console.log('request found');

    xhr.onreadystatechange = function() {
        if (this.readyState === 4 && this.status >= 200 && this.status < 400) {
            // console.log(xhr.response);
            func(xhr.response);
        }
        else {
            console.log('something went wrong... ((');
        }
    }
}