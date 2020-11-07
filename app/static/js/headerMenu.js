var username = document.getElementById('username');
var headerMenu = document.getElementById('header-menu');

function pasteUsername () {
    var url = '/current-user-info';
    var request = new XMLHttpRequest();

    request.open("GET", url, true);
    request.responseType = "json";
    request.send();

    request.onload = function() {
        username.textContent = '@' + request.response.username;
        let len = username.textContent.length * 10 + 10;
        if (len < 120) {
            len = 120;
        }
        headerMenu.style.width = len + 'px';
    }
}

pasteUsername()