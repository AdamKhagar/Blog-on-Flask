var buttonPanel = document.querySelector('.btn-panel');
var btnsOneInputText = buttonPanel.querySelectorAll('.btn.after-btn-one-input');
var newCategoryBtn = buttonPanel.querySelector('#new-category-btn');
var delCategoryBtn = buttonPanel.querySelector('#del-category-btn');
var addAdminBtn = buttonPanel.querySelector('#new-admin-btn');
var delPostBtn = buttonPanel.querySelector('#del-post-btn');
var userLockdownBtn = buttonPanel.querySelector('#user-lockdown-btn');
var advertiseBtn = buttonPanel.querySelector('#advertise-btn');

var formBox = document.querySelector('.form-box');
var closeFormBtn = formBox.querySelector('#come-back');
var form = formBox.querySelector('form')
var formTitle = form.querySelector('.title');
var inputBox = form.querySelector('.input-box');
var submit = document.getElementById('submit');
var formError = formBox.querySelector('.error');

var statistics = document.querySelector('.statistics');
var userCount = statistics.querySelector('.user-count');
var postCount = statistics.querySelector('.post-count');

urls = {
    newCategory: "/from-admin/new-category",
    delCategory: "/from-admin/del-categories", 
    addAdmin: "/from-admin/add-admin", 
    delPost: "/from-admin/del-post", 
    userLockdown: "/from-admin/user-lockdown", 
    adverise: "/from-admin/advertise",
    getCategories: "/get-categories", 
    getStatistics: "/get-statistics"
}

function statisticOnloadPaste() {
    let request = new XMLHttpRequest();
    request.open("GET", urls.getStatistics, true);
    request.responseType = 'json';
    request.send();
    request.onload = function() {
        userCount.textContent = request.response.users;
        postCount.textContent = request.response.posts;
        
    }
}

statisticOnloadPaste();

function closeForm() {
    buttonPanel.classList.remove("hidden");
    statistics.classList.remove("hidden")
    inputBox.textContent = '';
    formBox.classList.add("hidden");
    formError.textContent = '';
    formError.classList.add('hidden');
    submit.classList.remove('disable');
    submit.disabled = false;
}

closeFormBtn.addEventListener('click', closeForm);

function sendPostReq(url, requestData) {
    let request = new XMLHttpRequest();
    request.open("POST", url, true);
    request.setRequestHeader('Content-Type', 'application/json; charset=utf-8');
    request.send(JSON.stringify(requestData));
}

// newCategory, deletePost, addAdmin forms generete
btnsOneInputText.forEach(function(btn) {
    btn.addEventListener("click", function() {
        let data = btn.dataset;
        let label = document.createElement('label');
        let input = document.createElement('input');

        form.id = data.inputId;
        buttonPanel.classList.add('hidden');
        statistics.classList.add("hidden")
        formTitle.textContent = btn.textContent;
        input.type = 'text';
        input.required = true;
        label.for = input.id;
        label.textContent = data.inputLabel;
        inputBox.insertBefore(input, inputBox.lastChild);
        inputBox.insertBefore(label, inputBox.lastChild);
        submit.value = data.submitValue;
        formBox.classList.remove("hidden");

        // newCategory, deletePost, addAdmin forms submit 
        form.addEventListener('submit', function(evt) {
            evt.preventDefault();
            let titleText = formTitle.textContent;

            if (input.value != '__none__') {
                if (titleText == newCategoryBtn.textContent) {
                    sendPostReq(urls.newCategory, {name: input.value});
                } else if (titleText == addAdminBtn.textContent) {
                    sendPostReq(urls.addAdmin, {username: input.value});
                } else if (titleText == delPostBtn.textContent) {
                    sendPostReq(urls.delPost, {postLink: input.value});
                }
            }
            input.value = '__none__';
            closeForm();   
        })
    })
});


// deleteCategy form generate

delCategoryBtn.addEventListener("click", function() {
    let request = new XMLHttpRequest();

    request.open('GET', urls.getCategories, true);
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
        let field = document.createElement('div');
        field.classList.add('option');
        let optionInput = document.createElement('input');
        let optionLabel = document.createElement('label');
        optionInput.type = 'checkbox';
        optionInput.name = 'category';
        optionInput.classList.add('category-opt');
        optionInput.id = category.key;
        optionInput.classList.add('hidden');
        optionLabel.htmlFor = optionInput.id;
        optionLabel.textContent = category.value;
        field.appendChild(optionLabel);
        field.appendChild(optionInput);
        
        select.appendChild(field);
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
    radioSave.name = 'after-del-category';
    radioDel.name = 'after-del-category';
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
    statistics.classList.add("hidden")

    formBox.classList.remove('hidden');

    let allCategories = document.querySelectorAll('.category-opt');
    let checkedCategories = [];

    allCategories.forEach(function(category) {
        category.addEventListener('change', function() {
            let index = checkedCategories.indexOf(category.id);
            if (index == -1) {
                checkedCategories.push(category.id);
            } else {
                checkedCategories.slice(index, index);
            }
            if (checkedCategories.length == 0) {
                formError.textContent = 'Select at least one category you want to delete';
                formError.classList.remove('hidden');
                submit.classList.add('disable')
                submit.disabled = true;
            } else {
                formError.textContent = '';
                formError.classList.add('hidden');
                submit.classList.remove('disable');
                submit.disabled = false;
            }
        })
    })
}


// deleteCategory submit
function delCategoryFormSubmit() {
    let allCategories = document.querySelectorAll('.category-opt');
    let checkedCategories = [];
    let afterDeleteVars = document.querySelectorAll('.after-del-category');

    allCategories.forEach(function(category) {
        if (category.checked) {
            checkedCategories.push(category.id)
        }
    })

    let afterDelete;
    afterDeleteVars.forEach(function(variant) {
        if (variant.checked) {
            afterDelete = variant.value;
        }
    })
        
    if (checkedCategories.length == 0) {
        formError.textContent = 'Select at least one category you want to delete';
        formError.classList.remove('hidden');
        submit.classList.add('disable')
        submit.disabled = true;
    } else {
        requestData = {
            categories: checkedCategories,
            after: afterDelete
        };
        sendPostReq(urls.delCategory, requestData);
        buttonPanel.classList.remove('hidden');
        statistics.classList.remove("hidden")

        formBox.classList.add('hidden');
        inputBox.textContent = '';
    }
}


// userLockdown form generate

userLockdownBtn.addEventListener("click", function() {
    let data = userLockdownBtn.dataset;
    let label = document.createElement('label');
    let input = document.createElement('input');
    let inputTextField = document.createElement('div');
    inputTextField.classList.add("input-text-box")
    let questionBox = document.createElement('div');
    questionBox.id = 'question-box';
    let question = document.createElement('div');
    question.classList.add('question');
    question.textContent = "How long will the lockdown last?";
    let optionBox = document.createElement('div');
    optionBox.classList.add('option-box');

    inputBox.insertBefore(questionBox, inputBox.lastChild);
    questionBox.insertBefore(optionBox, questionBox.lastChild);
    questionBox.insertBefore(question, questionBox.lastChild);

    form.id = data.inputId;
    buttonPanel.classList.add('hidden');
    statistics.classList.add("hidden")
    formTitle.textContent = userLockdownBtn.textContent;
    input.type = 'text';
    input.required = true;
    label.for = input.id;
    label.textContent = data.inputLabel;
    
    inputBox.insertBefore(inputTextField, inputBox.lastChild);
    inputTextField.insertBefore(input, inputTextField.lastChild);
    inputTextField.insertBefore(label, inputTextField.lastChild);
    
    options = {
        '-1': 'forever',
        '365': 'year',
        '183': 'half a year', 
        '30': 'month', 
        '1': 'day'  
    }

    Object.keys(options).forEach(function(key, i) {
        let radioBox = document.createElement("div");
        let radioLabel = document.createElement("label");
        let radio = document.createElement("input");
        radio.type = "radio";
        radio.name = "period";
        radio.classList.add("period");
        radio.id = key;
        if (i == 0) {
            radio.checked = true;
        }
        radioLabel.htmlFor = key;
        radioLabel.textContent = options[key];
        
        optionBox.appendChild(radioBox);
        radioBox.appendChild(radio);
        radioBox.appendChild(radioLabel);
        
    })
    
    submit.value = data.submitValue;
    formBox.classList.remove("hidden");
    buttonPanel.classList.add("hidden");
    statistics.classList.add("hidden")

    form.addEventListener("submit", function(evt) {
        evt.preventDefault();
        lockdownFormSubmit()
    })
})

function lockdownFormSubmit(){
    let allRadio = document.querySelectorAll("input.period");
    let checkedRadioValue;
    let input = formBox.querySelector(".input-text-box input")
    allRadio.forEach(function(radio) {
        if (radio.checked) {
            checkedRadioValue = radio.id;
        }
    })
    let requestData = {
        period: checkedRadioValue,
        username: input.value
    }
    console.log(requestData)
    sendPostReq(urls.userLockdown, requestData);

    closeForm();
}