export let coordinates = null;

// Инициализация Яндекс Карты
function initMap() {
    let myMap = new ymaps.Map('map', {
        center: [56.838048312714704,60.60364972721357],
        zoom: 16,
        controls: []
    });

    let searchControl = new ymaps.control.SearchControl({
        options: {
            provider: 'yandex#map',
            noPlacemark: true
        }
    });

    searchControl.events.add('resultselect', function(e) {
        let index = e.get('index');
        searchControl.getResult(index).then(function(res) {

            coordinates = res.geometry.getCoordinates();
            myMap.geoObjects.removeAll();

            let placemark = new ymaps.Placemark(coordinates, {}, {});
            myMap.geoObjects.add(placemark);
        });
    })

    myMap.controls.add(searchControl);

    let eventLocation = document.getElementById('event-location');
    eventLocation.addEventListener('change', function() {
        update();
    })

    function update() {
        if (eventLocation.value) {
            searchControl.search(eventLocation.value);
        } else {
            myMap.geoObjects.removeAll();
            myMap.setCenter([56.838048312714704,60.60364972721357]);
            coordinates = null;
        }
    }
}

ymaps.ready(initMap);

