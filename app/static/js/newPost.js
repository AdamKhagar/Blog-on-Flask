var textPreview = document.querySelector('textarea.prev');
var textContent = document.querySelector('textarea.content');

textPreview.addEventListener('keyup', function(){
    var text = this.value;
    var qtyOfStrings = 0;
    for (let abc of text) {
        if (abc === '\n' || abc === '\r') {
            qtyOfStrings++;
        }
    }
    if(this.scrollTop > 0){
        this.style.height = this.scrollHeight + "px";
    }
});

textContent.addEventListener('keyup', function(){
    var text = this.value;
    var qtyOfStrings = 0;
    for (let abc of text) {
        if (abc === '\n' || abc === '\r') {
            qtyOfStrings++;
        }
    }
    if(this.scrollTop > 0){
        this.style.height = this.scrollHeight + "px";
    }
});

// заполнение select

function pasteOption() {
    let select = document.querySelector('select#category-select');
    let request = new XMLHttpRequest();

    function paste(category) {
        let option = document.createElement('option');
        option.id = category.key;
        option.textContent = category.value;
        select.appendChild(option);
    }

    request.open('GET', '/get-categories', true);
    request.responseType = 'json';
    request.send();

    request.onload = function () {
        let categories = request.response.categories;
        categories.forEach(category => paste(category));
    }
};

// pasteOption()