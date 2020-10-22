var flash = document.getElementById('flash-message');
var closeFlash = document.getElementById('flash-close');

closeFlash.onclick = function () {
    flash.remove();
}