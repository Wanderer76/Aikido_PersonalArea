addNewMembers();
function addNewMembers() {
    let studData = JSON.parse(window.sessionStorage.getItem('new_aiki'));
    console.log(studData);
    if (studData == null) return;

    let defRow = document.getElementById('default-row');
    for (let i = 0; i < studData.length; i++) {
        let output = document.createElement('tr');
        output.innerHTML = studData[i].second_name !== undefined ?
        '<td></td>' +
        '<td>'+ studData[i].surname + ' ' + studData[i].name + ' ' + studData[i].second_name +'</td>' +
        '<td>'+ setDateFormat(studData[i].birthdate) +'</td>' +
        '<td>' +
        '</td>' +
        '<td class="checkbox-cell"><input type="checkbox" class="checkbox" checked></td>' :

        '<td></td>' +
        '<td>'+ studData[i].surname + ' ' + studData[i].name +'</td>' +
        '<td>'+ setDateFormat(studData[i].birthdate) +'</td>' +
        '<td>' +
        '</td>' +
        '<td class="checkbox-cell"><input type="checkbox" class="checkbox" checked></td>';
        defRow.parentElement.insertBefore(output, defRow.nextSibling);
    }
    storage.removeItem('new_aiki');
}
