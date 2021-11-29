let sendButton = document.getElementById('send-button');
let participants = [];

sendButton.onclick = function () {
    let checkboxes = document.querySelectorAll('.checkbox');
    checkboxes.forEach(element => getRowInfo(element));
    let sender = new XMLHttpRequest();
    let url = 'http://localhost:8000/api/v1/events/requests/create/';
    sender.open('POST', url);
    sender.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'));
    console.log(JSON.stringify(participants));
    sender.send(JSON.stringify(participants));
    location.href = '../html/service_page.html';
}

function getRowInfo(checkbox) {
    if (checkbox.checked){
        let cols = checkbox.parentElement.parentElement.getElementsByTagName("td");
        let birthdate = cols[2].textContent.split('.');
        participants.push({
            "name": cols[1].textContent.split(" ")[0],
            "surname" : cols[1].textContent.split(" ")[1],
            "member_id" : cols[0].textContent.substring(1, cols[0].textContent.length),
            "birthdate" : birthdate[2]+'-'+birthdate[1]+'-'+birthdate[0],
            "event_name" : document.getElementById('event-name').textContent,
            "trainer_id" : storage.getItem("myId")
        });
    }
}
