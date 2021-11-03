let button = document.querySelector('.menu-btn');
let menu = document.querySelector('.menu');
let content = document.querySelector('.content');
let isOpened = false;
button.onclick = function() {
  if (!isOpened) {
    isOpened = !isOpened;
    menu.classList.add('menu_active');
    content.classList.add('content_active');
  } else {
    isOpened = !isOpened;
    menu.classList.remove('menu_active');
    content.classList.remove('content_active');
  }
}


