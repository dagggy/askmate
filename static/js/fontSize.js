const el = document.getElementsByName('body');
const style = window.getComputedStyle(el, null).getPropertyValue('font-size');
const fontSize = parseFloat(style);

function enlargeFont(){
    if(el.style.fontSize <15){
        el.style.fontSize = (fontSize + 1) + 'px';
    }
}

function ensmallenFont(){
    if(el.style.fontSize <3){
        el.style.fontSize = (fontSize - 1) + 'px';
    }
}