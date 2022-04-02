function getAllInfo() {
    let clubName = document.getElementById("club-name").value;
    let area = document.getElementById("area").value;
    let city = document.getElementById("city").value;

    let coaches = document.getElementsByName("coach-selector");
    let coachesArr = []
    coaches.forEach(function (item) {
        if (item.value !== "none")
            coachesArr.push(item.value);
    });

    let fd = createFormDataImage(currentImage, 'club-icon');
    let json = {"name" : clubName, "city" : city, "area" : area, "main_trainers" : Array.from(new Set(coachesArr))};
    fd.append('jsonInfo', JSON.stringify(json));
    return fd;

}

function createFormDataImage(imgFile, name) {
    let fd = new FormData();
    fd.append(name, imgFile);
    return fd;
}

function hideErrorMessage() {
    document.getElementById("error-message").classList.add('hidden');
}


function sendAllInfo() {
    let fd = getAllInfo();
    let parsed = JSON.parse(fd.get('jsonInfo'));

    if (parsed['name'] === "" || parsed['city'] === "" || parsed['area'] === "" || parsed['main_trainers'].length === 0) {
        let message = document.getElementById("error-message");
        message.classList.remove('hidden');
    }
    else {
        console.log('Sending was started!');
        console.log(fd.get('club-icon'));
        console.log(fd.get('jsonInfo'))
    }
}


function updateImageLogo() {
    if (this.files &&
        this.files.length) {
        previewLogo.src = window.URL.createObjectURL(this.files[0]);
        currentImage = this.files[0];
        let attribute = currentImage.width > currentImage.height ? 'height' : 'width';
        previewLogo.setAttribute(attribute, '90%');
    } else {
        previewLogo.setAttribute('width', '90%');
        previewLogo.src = "../assets/empty-club-icon.png";
    }
}

let currentImage;
const inputLogo = document.getElementById('logo-uploader');
const previewLogo = document.getElementById('logo-icon-preview');
inputLogo.addEventListener('change', updateImageLogo);

function changeGridAreaOnFirstElement(className, value) {
    let selectorBlock = document.getElementsByClassName(className)[0];
    selectorBlock.style.gridTemplateAreas = value;
}

// Добавление нового селектора
function addMoreCoach() {
    let form = document.getElementsByClassName('forms')[0];
    let newSelectObject = document.createElement('select')
    newSelectObject.classList.add('coach-selector');
    newSelectObject.classList.add('coach-selector-add');
    newSelectObject.name = 'coach-selector';
    newSelectObject.innerHTML = "<option value=\"none\" selected>Выберите тренера</option>"

    let selectors = document.getElementsByClassName('coach-selector');
    let butt = document.getElementsByClassName('add')[0];
    let lastSelector = selectors[selectors.length-1];
    lastSelector.classList.remove('coach-selector-add')
    butt.parentElement.insertBefore(newSelectObject, butt);
    fillNewSelectors(newSelectObject);
    let parameterString = ''
    for (let i =0; i < selectors.length-1; i++) {
        parameterString += '"coach-name' + i + ' coach-name' + i + ' coach-name'+i+'"';
        selectors[i].style.gridArea = 'coach-name' + i;
    }
    parameterString += '"coach-name-add coach-name-add add"';
    console.log(parameterString);
    changeGridAreaOnFirstElement('coach-selector-block', parameterString);
}



function fillNewSelectors(selector) {
    let coaches = [{id: '001', name: "Somebody Coach 1"}, {id: '002', name: "Somebody Coach 2"}]
    for (let i = 0; i < coaches.length; i++) {
        let option = document.createElement('option');

            option.value = coaches[i].id;
            option.textContent = coaches[i].name + " #" + coaches[i].id;

        insertAfter(option, selector.lastElementChild);
    }
}

function insertAfter(newNode, existingNode) {
    existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
}

fillNewSelectors(document.getElementsByClassName('coach-selector')[0]);