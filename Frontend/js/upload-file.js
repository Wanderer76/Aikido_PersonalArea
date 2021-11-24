let uploadButton = document.getElementById('upload');
let filename = window.sessionStorage.getItem("activityName");
let uploadUrl = 'api/v1/admin/seminar/load/' + filename + '/';
let uploader = new XMLHttpRequest();

uploader.onreadystatechange = state => { console.log(uploader.status); }

uploadButton.onchange = function () {
    let file = document.getElementById('upload').files[0];
    console.log(file.name);
    let formData = new FormData();
    formData.append(filename, file, filename + '.' + file.name.split('.').pop())
    console.log(formData.get(filename).name);

    uploader.open('POST', uploadUrl);
    uploader.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'))
    uploader.send(formData);
}
