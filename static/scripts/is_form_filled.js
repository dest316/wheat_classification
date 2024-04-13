const values = document.querySelectorAll('.item-value')
const main = () => {
    let isFilledIn = true;
    values.forEach(
        (inputElement) => {
            if (inputElement.value === '') {
                isFilledIn = false;
            }
        }
    )
    if (isFilledIn) {
        document.getElementById('submit-button').removeAttribute('disabled');
    }
}
values.forEach((item) => {
    item.addEventListener('blur', main);
})