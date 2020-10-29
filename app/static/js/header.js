var headerBox = document.getElementById('header-box');
var logo = document.getElementById('logo');

logo.addEventListener('mouseover', function() {
    headerBox.style.backgroundColor = '#3498db'
})

logo.addEventListener('mouseout', function() {
    headerBox.style.backgroundColor = '#34495e';
})



