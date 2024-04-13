const class_button = document.getElementById('classes-button')
const property_button = document.getElementById('properties-button')
const relevant_button = document.getElementById('relevant-values-button')
const properties_classes_button = document.getElementById('properties-classes-button')
const relevant_class_button = document.getElementById('relevant-values-for-classes-button')
const check_button = document.getElementById('check-button')
class_button.addEventListener('click', () => {
    window.location.href = window.location.origin + '/editor'
})
property_button.addEventListener('click', () => {
    window.location.href = window.location.origin + '/editor/property'
})
relevant_button.addEventListener('click', () => {
    window.location.href = window.location.origin + '/editor/relevant'
})
properties_classes_button.addEventListener('click', () => {
    window.location.href = window.location.origin + '/editor/property-class'
})
relevant_class_button.addEventListener('click', () => {
    window.location.href = window.location.origin + '/editor/relevant-class'
})
check_button.addEventListener('click', () => {
    window.location.href = window.location.origin + '/editor/completeness'
})
if (window.location.href === window.location.origin + '/editor') {
    class_button.classList.add('active')
} else if (window.location.href === window.location.origin + '/editor/property') {
    property_button.classList.add('active')
} else if (window.location.href === window.location.origin + '/editor/relevant') {
    relevant_button.classList.add('active')
} else if (window.location.href === window.location.origin + '/editor/property-class') {
    properties_classes_button.classList.add('active')
} else if (window.location.href === window.location.origin + '/editor/relevant-class') {
    relevant_class_button.classList.add('active')
} else if (window.location.href === window.location.origin + '/editor/completeness') {
    document.getElementById('content').style.overflowY = 'auto'
}

