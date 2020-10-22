var buttonPanel = document.querySelector('.btn-panel');
var btnsOneInputText = buttonPanel.querySelectorAll('.btn.after-btn-one-input');
var newCategoryBtn = buttonPanel.querySelector('#new-category-btn');
var delCategoryBtn = buttonPanel.querySelector('#del-category-btn');
var addAdminBtn = buttonPanel.querySelector('#new-admin-btn');
var delPostBtn = buttonPanel.querySelector('#del-post-btn');
var userLockdownBtn = buttonPanel.querySelector('#user-lockdown-btn');
var advertiseBtn = buttonPanel.querySelector('#advertise-btn');

var form = document.querySelector('form');
var closeFormBtn = form.querySelector('#come-back');
var formTitle = form.querySelector('.title');
var inputBox = form.querySelector('.input-box');
var submit = form.querySelector('input[type=submit]')

closeFormBtn.addEventListener('click', function() {
    buttonPanel.classList.remove("hidden");
    inputBox.textContent = '';
    form.classList.add("hidden");
});

btnsOneInputText.forEach(function(btn) {
    btn.addEventListener("click", function() {
        let data = btn.dataset;
        let label = document.createElement('label');
        let input = document.createElement('input');

        form.id = data.inputId;
        buttonPanel.classList.add("hidden");
        formTitle.textContent = btn.textContent;
        input.type = 'text';
        label.for = input.id;
        label.textContent = data.inputLabel;
        inputBox.insertBefore(input, inputBox.lastChild);
        inputBox.insertBefore(label, inputBox.lastChild);
        submit.value = data.submitValue;
        form.classList.remove("hidden");
    })
});

