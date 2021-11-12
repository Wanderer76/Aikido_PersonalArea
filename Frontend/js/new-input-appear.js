let d = document;
let last_id = 0;
function add_value_f() {

    // находим нужную таблицу
    let tbody = d.getElementById('v_table').getElementsByTagName('tbody')[0];
    for (let i = 0; i < tbody.children.length; i++) {
        tbody.children[i].classList.remove('last_value');
    }

    // создаем строку таблицы и добавляем ее
    let row = d.createElement("tr");
    tbody.appendChild(row);

    // создаем ячейки в вышесозданной строке
    let td1 = d.createElement("td");
    let td2 = d.createElement("td");
    let td3 = d.createElement("td");
    let td4 = d.createElement("td");

    row.appendChild(td1).setAttribute("class", "last_value");
    row.appendChild(td2).setAttribute("class", "last_value");
    row.appendChild(td3).setAttribute("class", "last_value");
    row.appendChild(td4).setAttribute("class", "last_value");

    last_id = last_id + 1;

    // добавляем поля в ячейки
    td1.innerHTML = '<input type="text" name="surname['+last_id+']" placeholder="Фамилия">';
    td2.innerHTML = '<input type="text" name="name['+last_id+']" placeholder="Имя">';
    td3.innerHTML = '<input type="text" name="second_name['+last_id+']" placeholder="Отчество">';
    td4.innerHTML = '<input type="text" name="birthdate['+last_id+']" placeholder="ДР">';
}

function remove_value_f() {
    let rows = d.getElementById('v_table').getElementsByTagName('tr');
    if (rows.length > 1) {
        let last_index = rows.length - 1;
        rows[last_index].remove();
    }
}
