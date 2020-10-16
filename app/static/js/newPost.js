var textarea = document.querySelector('textarea');

textarea.addEventListener('keyup', function(){
    var text = this.value;
    var qtyOfStrings = 0;
    for (let abc of text) {
        if (abc === '\n' || abc === '\r') {
            qtyOfStrings++;
        }
    }
    var heihgtValue = 24 * (1 + qtyOfStrings);
    if (heihgtValue <= 210) {
        heihgtValue = 210;
    } 
    textarea.style.height = heihgtValue + 'px';
});