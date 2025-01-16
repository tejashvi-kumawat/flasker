document.addEventListener('DOMContentLoaded', () => {
    const pendingBtn = document.getElementById('pending-btn');
    const completedBtn = document.getElementById('completed-btn');
    const cardsContainer = document.getElementById('cards-container');
    const pointsElement = document.getElementById('points');
    
    let cardsVisible = false;
    let currentView = 'none';

    const pendingTasks = [
        { title: 'Pending Task 1', description: 'Sample 1' },
        { title: 'Pending Task 2', description: 'Sample 2' },
        { title: 'Pending Task 3', description: 'Sample 3' },
        { title: 'Pending Task 4', description: 'Sample 4' },
        { title: 'Pending Task 5', description: 'Sample 5' }
    ];

    const completedTasks = [
        { title: 'Completed Task 1', description: 'Sample 1' },
        { title: 'Completed Task 2', description: 'Sample 2' },
        { title: 'Completed Task 3', description: 'Sample 3' },
        { title: 'Completed Task 4', description: 'Sample 4' },
        { title: 'Completed Task 5', description: 'Sample 5' }
    ];

    pointsElement.innerText = completedTasks.length;

    function displayCards(tasks) {
        cardsContainer.innerHTML = '';
        tasks.forEach(task => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `<h3>${task.title}</h3><p>${task.description}</p>`;
            cardsContainer.appendChild(card);
        });
        cardsContainer.classList.remove('cards-hidden');
    }

    pendingBtn.addEventListener('click', () => {
        if (currentView === 'pending') {
            cardsContainer.classList.add('cards-hidden');
            currentView = 'none';
        } else {
            displayCards(pendingTasks);
            currentView = 'pending';
        }
    });

    completedBtn.addEventListener('click', () => {
        if (currentView === 'completed') {
            cardsContainer.classList.add('cards-hidden');
            currentView = 'none';
        } else {
            displayCards(completedTasks);
            currentView = 'completed';
        }
    });

    const titleText = document.getElementById('title');
    const title = 'eDC Campus Ambassador Program';
    let index = 0;
    
    titleText.innerText = '';

    function typeWriter() {
        if (index < title.length) {
            titleText.innerHTML += title.charAt(index);
            index++;
            setTimeout(typeWriter, 100);
        }
    }

    typeWriter();
});
$(document).ready(function() {
    $('#inputForm').on('submit', function(e) {
        e.preventDefault();  // Prevent the form from submitting the traditional way
        
        // Get the value from the input field
        var user_input = $('#user_input').val();
        
        // Send the input data to Flask using AJAX
        $.ajax({
            url: '/submit', 
            type: 'POST',
            data: { user_input: user_input },
            success: function(response) {
                // Update the page with the response (display user input)
                $('#result').html('<h1>You entered: ' + response + '</h1>');
            }
        });
    });
});