function enlargeFont(className){
    let txt = document.getElementById(className);
    let style = window.getComputedStyle(txt, null).getPropertyValue('font-size')
    let currentSize = parseFloat(style);
    console.log(currentSize)
    if(currentSize < 20){
        txt.style.fontSize = (currentSize + 1) + 'px'
    }
}

function ensmallenFont(className){
    let txt = document.getElementById(className);
    let style = window.getComputedStyle(txt, null).getPropertyValue('font-size')
    let currentSize = parseFloat(style);
    console.log(currentSize)
    if(currentSize > 12){
        txt.style.fontSize = (currentSize - 1) + 'px'
    }
}