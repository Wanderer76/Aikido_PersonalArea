let seminarName = window.sessionStorage.getItem("activityName");
let downloadUrl = 'http://localhost:8000/api/v1/admin/seminar/download/'+ seminarName + '/';
let downloadButton = document.getElementById('download');
let downloader = new XMLHttpRequest();
let data;


downloadButton.onclick = function () {
    downloader.open('GET', downloadUrl);
    downloader.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'))
    downloader.send();
    console.log("downloading...");

    // window.open(data);  //раскоментировать когда будет загрузка файлов

}

downloader.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        data = downloader.response;
        console.log(data);
        window.open(data);
    }
}
