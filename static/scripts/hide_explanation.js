const icon = document.getElementById('question_icon');
const explanation = document.getElementById('explanation');
const cross = document.getElementById('cross_icon');
icon.addEventListener('click', () => {
    explanation.style.visibility = 'visible';
})
cross.addEventListener('click', () => {
    explanation.style.visibility = 'hidden';
})
