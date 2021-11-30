const url = "http://localhost:8000/api/v1/events/requests/create/";
let add_to_applic = document.getElementById('add_to_applic');
let table = document.getElementById('v_table');

add_to_applic.onclick = function (){
    let rows = table.getElementsByTagName('tr');
    let last_element = rows.length;
    let result = [];
    for(let i = 0; i < last_element; i++){
        let row = rows[i].getElementsByTagName('td');
        let second_name = row[2].getElementsByTagName('input')[0].value;
        let element = {
            "name":row[1].getElementsByTagName('input')[0].value,
            "surname":row[0].getElementsByTagName('input')[0].value,
            "birthdate":row[3].getElementsByTagName('input')[0].value
        };
        if (second_name !== ''){
            element['second_name'] = second_name;
        }
        result.push(element);
    }
    window.sessionStorage.setItem('new_aiki',JSON.stringify(result));
    console.log('good!')
}
