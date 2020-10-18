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
    var heihgtValue = 24 * (1 + qtyOfStrings);
    if (heihgtValue <= 150) {
        heihgtValue = 150;
    } 
    textPreview.style.height = heihgtValue + 'px';
});

textContent.addEventListener('keyup', function(){
    var text = this.value;
    var qtyOfStrings = 0;
    for (let abc of text) {
        if (abc === '\n' || abc === '\r') {
            qtyOfStrings++;
        }
    }
    var heihgtValue = 24 * (1 + qtyOfStrings);
    if (heihgtValue <= 300) {
        heihgtValue = 300;
    } 
    textContent.style.height = heihgtValue + 'px';
});