let seminarName = window.sessionStorage.getItem("activityName");
let downloadUrl = 'http://localhost:8000/api/v1/admin/seminar/download/'+ seminarName + '/';
let downloadButton = document.getElementById('download');
let downloader = new XMLHttpRequest();
downloader.responseType = 'blob';
let data;
let isAttributeSet = false;


downloadButton.onclick = function () {
    downloader.open('GET', downloadUrl);
    downloader.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'))
    downloader.send();
}

downloader.onload = function () {
    saveAs(this.response, seminarName+'.xlsx');
}

function saveAs(blob, filename) {
     var a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";

    var url = window.URL.createObjectURL(blob);
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

