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

function showDeleteCategoryForm(categories) {
    let data = delCategoryBtn.dataset;
    let select = document.createElement('div');
    let selectLabel = document.createElement('label')

    formTitle.textContent = delCategoryBtn.textContent;
    form.id = 'del-category-form';

    select.id = 'del-category-select';
    selectLabel.htmlFor = select.id;
    selectLabel.textContent = data.inputLabel;

    submit.value = data.submitValue;

    categories.forEach(function(category) {
        // console.log(category)
        let field = document.createElement('div');
        field.classList.add('option');
        let optionInput = document.createElement('input');
        let optionLabel = document.createElement('label');
        optionInput.type = 'checkbox';
        optionInput.classList.add('category-opt');
        optionInput.id = category.key;
        optionInput.classList.add('hidden');
        optionLabel.htmlFor = optionInput.id;
        optionLabel.textContent = category.value;
        field.insertBefore(optionLabel, field.lastChild);
        field.insertBefore(optionInput, field.lastChild);
        
        select.insertBefore(field,select.lastChild);
    })
    

    let questionBox = document.createElement('div');
    let question = document.createElement('div');
    let radioDel = document.createElement('input');
    let radioSave = document.createElement('input');
    let labelDel = document.createElement('label');
    let labelSave = document.createElement('label');
    let optionDel = document.createElement('div');

    optionDel.classList.add('radio-opt');

    let optionSave = optionDel.cloneNode(true);

    questionBox.id = 'question-box';
    question.textContent = 'What to do with the posts of deleted categories?';
    question.classList.add('question');
    radioDel.type = 'radio';
    radioSave.type = 'radio';
    radioDel.classList.add('after-del-category');
    radioSave.classList.add('after-del-category');
    radioDel.id = 'del-posts';
    radioSave.id = 'save-posts';
    radioDel.value = false;
    radioSave.value = true;
    radioSave.checked = true;

    labelDel.htmlFor = radioDel.id;
    labelSave.htmlFor = radioSave.id;
    labelDel.textContent = 'Delete this posts';
    labelSave.textContent = 'Change categories to "without category"'

    inputBox.insertBefore(questionBox, inputBox.lastChild);
    
    questionBox.insertBefore(optionDel, questionBox.lastChild);
    questionBox.insertBefore(optionSave, questionBox.lastChild);

    optionSave.insertBefore(labelSave, optionSave.lastChild);
    optionSave.insertBefore(radioSave, optionSave.lastChild);
    optionDel.insertBefore(labelDel, optionDel.lastChild);
    optionDel.insertBefore(radioDel, optionDel.lastChild);

    questionBox.insertBefore(question, questionBox.firstChild);

    inputBox.insertBefore(select, inputBox.lastChild);
   
    inputBox.insertBefore(selectLabel, select);
    buttonPanel.classList.add('hidden');
    form.classList.remove('hidden');
}

function delCategoryFormSubmit() {
    let allCategories = document.querySelectorAll('.category-opt');
    let checkedCatereies = [];
    let afterDeleteVars = document.querySelectorAll('.after-del-category');
    
    allCategories.forEach(function(category) {
        if (category.checked) {
            checkedCatereies.push(category.id);
        }
    })

    let afterDelete;
    afterDeleteVars.forEach(function(variant) {
        if (variant.checked) {
            afterDelete = variant.value;
        }
    })

    requestData = {
        categories: checkedCatereies,
        after: afterDelete
    };

    let postURL = 'from-admin/delete-categories';
    let postReq = new XMLHttpRequest();

    postReq.open('POST', postURL, true);
    postReq.send(requestData)
}

delCategoryBtn.addEventListener("click", function() {
    let url = 'http://localhost:5000/get_categories';
    let request = new XMLHttpRequest();

    request.open('GET', url, true);
    request.responseType = 'json';
    request.send();
    request.onload = function () {
        let categories = request.response.categories
        
        showDeleteCategoryForm(categories)

        let delCategoryForm = document.getElementById('del-category-form');
        delCategoryForm.addEventListener('submit', function(evt) {
            evt.preventDefault();
            delCategoryFormSubmit()
        });
    }
})

