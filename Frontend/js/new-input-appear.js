function add_field(){

    let x = document.querySelector('.new_person');
    // создаем новое поле ввода
    let new_field = document.createElement("input");
    // установим для поля ввода тип данных 'text'
    new_field.setAttribute("type", "text");
    // установим имя для поля ввода
    new_field.setAttribute("name", "text_field[]");
    // определим место вствки нового поля ввода (перед каким элементом его вставить)
    let pos = x.childElementCount;

    // добавим поле ввода в форму
    x.insertBefore(new_field, x.childNodes[pos]);
}

let input = document.querySelector('input');
input.addEventListener("change", function() {
    if (input.length > 0) {
        input.classList.remove(new_person);
        add_field();
    }
})