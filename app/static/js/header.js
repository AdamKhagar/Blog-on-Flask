var username = document.getElementById('username');
var headerMenu = document.getElementById('header-menu');
var headerBox = document.getElementById('header-box');
var logo = document.getElementById('logo');

function pasteUsername () {
    var url = '/current_user_info';
    var request = new XMLHttpRequest();

    request.open("GET", url, true);
    request.responseType = "json";
    request.send();

    request.onload = function() {
        username.textContent = '@' + request.response.username;
        let len = username.textContent.length * 10;
        if (len < 120) {
            len = 120;
        }
        headerMenu.style.width = len + 'px';
    }
}

pasteUsername()

logo.addEventListener('mouseover', function() {
    headerBox.style.backgroundColor = '#3498db'
})

logo.addEventListener('mouseout', function() {
    headerBox.style.backgroundColor = '#34495e';
})