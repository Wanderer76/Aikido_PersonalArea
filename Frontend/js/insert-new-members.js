addNewMembers();

function addNewMembers() {
    let studData = storage.getItem('new-members');
    if (studData == null) return;

    let defRow = document.getElementById('default-row');
    for (let i = 0; i < studData.length; i++) {
        let output = document.createElement('tr');
        output.innerHTML =
        '<td>#'+ studData[i].id +'</td>' +
        '<td>'+ studData[i].name + ' ' + studData[i].surname +'</td>' +
        '<td>'+ setDateFormat(studData[i].birthdate) +'</td>' +
        '<td>' +
            '<div class="degree ku-'+ studData[i].ku +'">'+ studData[i].ku+' кю <br><span  class="dateInBlock">'+ setDateFormat(studData[i].attestation_date) +'</span></div>' +
        '</td>' +
        '<td class="checkbox-cell"><input type="checkbox" class="checkbox"></td>';
        defRow.parentElement.insertBefore(output, defRow);
    }
    storage.remove('new-members');
}