let labels = document.querySelectorAll('.white-label, .black-label')

labels[0].addEventListener('click', function () {
    labels[0].classList.add('btn-primary')
    labels[1].classList.remove('btn-primary')
})

labels[1].addEventListener('click', function () {
    labels[1].classList.add('btn-primary')
    labels[0].classList.remove('btn-primary')
})
