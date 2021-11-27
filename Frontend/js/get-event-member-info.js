let getter = new XMLHttpRequest();
LoadMemberEventInfo();
function LoadMemberEventInfo() {
    let urlEventInfo = 'api/v1/events/requests/'+ storage.getItem("activityName") +'/';
    getter.open('GET', urlEventInfo);
    getter.setRequestHeader('Authorization', 'Token ' + storage.getItem('user_token'))
    getter.send();
}

getter.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        console.log(getter.response);
    }
}

