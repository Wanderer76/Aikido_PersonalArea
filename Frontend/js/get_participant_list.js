let sendButton = document.getElementById('send-button');
let checkboxes = document.querySelectorAll('.checkbox');
let participants = [];
sendButton.onclick = function () {
    checkboxes.forEach(element => getRowInfo(element));
    console.log(participants);
}

function getRowInfo(checkbox) {
    if (checkbox.checked){
        cols = checkbox.parentElement.parentElement.getElementsByTagName("td");
        participants.push({"name":cols[0].split(" ")[0],
            "surname" : cols[0].split(" ")[1],
            "birthdate" : cols[1]});
    }
}
