const changeBackground = (elem) => {
    let changedElem = elem.getAttribute('id') === 'left' ? document.getElementById('right') : document.getElementById('left')
    let elem_id = elem.getAttribute('id')
    changedElem.style.backgroundColor = 'darkgrey'
    elem.style.backgroundColor = elem_id === 'left' ? 'rgb(203, 1, 51)' : 'rgb(0, 47, 85)'
}


const blocks = document.getElementsByClassName('main-item')
for (let elem of blocks) {
    elem.addEventListener("mouseover", () => {changeBackground(elem)})
}
