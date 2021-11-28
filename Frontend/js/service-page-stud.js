const stud_url = "http://localhost:8000/api/v1/account/trainer_students/";
let stud_xhr = new XMLHttpRequest();
let d = document;
let last_id = 0;
 stud_xhr.responseType = 'json';

stud_xhr.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        let stud_data = stud_xhr.response;
        setOutputParams(stud_data["список учеников"]);
        setDefaultValue(stud_data["список учеников"]);
        console.log(stud_data);
    }
}
stud_xhr.open("GET", stud_url, true);
stud_xhr.setRequestHeader('Authorization', 'Token ' + window.sessionStorage.getItem('user_token'));
stud_xhr.send();
function setOutputParams(jsonData) {
    for(let i = 0; i < jsonData.length; i++){
        console.log(jsonData[i]);
        setStudInfo(jsonData[i]);
    }
}
function setStudInfo(stud_data){
    let def = document.getElementById('default-row');
    let output = document.createElement("tr");
    output.innerHTML = '<td class="fio-2" style="width: 320px;">'+ stud_data.surname + ' ' + stud_data.name +'</td>' +
    '<td class="bordered-3" style="width: 400px;"><div class="degree ku-'+ stud_data.ku +' row col-12 col-md-8">' +
        '<div class="col-2 row abc">'+ stud_data.ku +' кю</div><div class="col-3 date">' + setDateFormat(stud_data.attestation_date) + '</div>' +
    '</div></td>' +
    '<td class="bordered-3" style="width: 250px;"><button class="col-4 col-md-5 belt-id-1" id="belt-id-1">' + '#' + stud_data.id + '</button></td>';
    def.parentElement.insertBefore(output, def);
}
function setDateFormat(strDate) {
    let date = new Date(strDate);

    let month = date.getMonth()+1;
    if (month < 10) {month = '0' + month};

    let day = date.getDate()
    if (day < 10) {day = '0' + day}
    return day + '.' + month + '.' + date.getFullYear();
}

function setDefaultValue(stud_data){
    if(stud_data.length == 0){
        let def = document.getElementById('default_value');
        def.textContent = 'У вас пока нет учеников :(';
    }
}