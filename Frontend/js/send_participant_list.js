let sendButton = document.getElementById('send-button');
let checkboxes = document.querySelectorAll('.checkbox');
let participants = [];

sendButton.onclick = function () {
    checkboxes.forEach(element => getRowInfo(element));
    let sender = new XMLHttpRequest();
    let url = 'http://localhost:8000/api/v1/events/requests/create/';
    sender.open('GET', url);
    sender.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'))
    sender.send(JSON.stringify(participants));
}

function getRowInfo(checkbox) {
    if (checkbox.checked){
        cols = checkbox.parentElement.parentElement.getElementsByTagName("td");
        participants.push({
            "name": cols[1].textContent.split(" ")[0],
            "surname" : cols[1].textContent.split(" ")[1],
            "member_id" : cols[0].textContent.substring(1, cols[0].textContent.length),
            "birthdate" : cols[2].textContent,
            "event_name" : document.getElementById('event-name').textContent,
            "trainer_id" : storage.getItem("myId")
        });
    }
}
