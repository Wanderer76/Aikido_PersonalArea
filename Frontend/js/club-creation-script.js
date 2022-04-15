let coaches;
getRequest('http://localhost:8000/api/v1/account/trainers/', fillCoaches);

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

    let fd = createFormDataImage(currentImage, 'logo');
    fd.append("name", clubName);
    fd.append("city", city);
    fd.append("area", area);
    if (coachesArr.length !== 0)
        for (let coach_id of coachesArr) {
            fd.append("main_trainers", coach_id);
            console.log('add ' + coach_id + 'trainer');
        }


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


function sendAllInfo(url, method) {
    let fd = getAllInfo();
    console.log()
    console.log('Sending was started!');
    if (fd.get("name") === "" || fd.get("city") === "" || fd.get("area") === "")
        document.getElementById("error-message").classList.remove('hidden');
    else {
        postWithoutAnswer(url, fd, method, function () {location.href = "../html/clubs.html"});
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
function addMoreCoach(selectedCoachId = undefined) {
    console.log('selectedCoachId='+selectedCoachId);
    let form = document.getElementsByClassName('forms')[0];
    let newSelectObject = document.createElement('select')
    newSelectObject.classList.add('coach-selector');
    newSelectObject.classList.add('coach-selector-add');
    newSelectObject.name = 'coach-selector';
    newSelectObject.innerHTML = '<option value="none" selected>Выберите тренера</option>'


    let selectors = document.getElementsByClassName('coach-selector');
    let butt = document.getElementsByClassName('add')[0];
    let lastSelector = selectors[selectors.length-1];
    lastSelector.classList.remove('coach-selector-add')
    butt.parentElement.insertBefore(newSelectObject, butt);
    fillNewSelectors(newSelectObject, selectedCoachId);
    let parameterString = ''
    for (let i =0; i < selectors.length-1; i++) {
        parameterString += '"coach-name' + i + ' coach-name' + i + ' coach-name'+i+'"';
        selectors[i].style.gridArea = 'coach-name' + i;
    }
    parameterString += '"coach-name-add coach-name-add add"';
    console.log(parameterString);
    changeGridAreaOnFirstElement('coach-selector-block', parameterString);
}



function fillNewSelectors(selector, coachId) {
    for (let i = 0; i < coaches.length; i++) {
        let option = document.createElement('option');
        if (coachId !== undefined && Number(coachId) === coaches[i]['id']) {
            console.log('Yes! Selected');
            option.selected = true;
        }
        option.value = coaches[i]['id'];
        option.textContent = coaches[i]['name'] + coaches[i]['surname'] + coaches[i]['second_name'] + " #" + coaches[i].id;

        insertAfter(option, selector.lastElementChild);
    }
}

function insertAfter(newNode, existingNode) {
    existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
}


function fillCoaches(data) {
    coaches = JSON.parse(data)
    fillNewSelectors(document.getElementsByClassName('coach-selector')[0]);
}




