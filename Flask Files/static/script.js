document.addEventListener('DOMContentLoaded', () => {
    const titleText = document.getElementById('title');
    const title = 'Event Passes for Tryst Day 1';
    let index = 0;

    titleText.innerText = '';

    function typeWriter() {
        if (index < title.length) {
            titleText.innerHTML += title.charAt(index);
            index++;
            setTimeout(typeWriter, 50);
        }
    }

    typeWriter();
});