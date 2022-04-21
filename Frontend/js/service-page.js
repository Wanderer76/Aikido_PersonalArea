const url = "http://localhost:8000/api/v1/account/profile/";
getRequest(url, setTrainerBaseInfo)

function setTrainerBaseInfo(sendingData){
    let data = JSON.parse(sendingData);
    console.log(data);
    document.getElementById('region').textContent = data.area;
    document.getElementById('city').textContent = data.city;
    document.getElementById('club').textContent = data.club;
    document.getElementById('stud-count').textContent = data.members;
}


