// Initialize the WebSocket connection
const socket = io('http://laundry-app.chost.com.ua', {
    transports: ['websocket', 'polling']
});

// Handle connection event
socket.on('connect', () => {
    console.log('Connected to WebSocket server');
});

// Handle connection error event
socket.on('connect_error', (error) => {
    console.error('Connection Error:', error);
});

// Handle initialization of bookings
socket.on('init_bookings', function(data) {
    updateSlots(data);
});

// Handle update of bookings
socket.on('update_bookings', function(data) {
    const slotId = `${data.day}-${data.slot}`;
    const input = document.getElementById(slotId);
    if (data.name.toLowerCase() === 'free') {
        input.value = '';
        input.placeholder = 'free';
    } else {
        input.value = data.name;
        input.setAttribute('readonly', 'true');
        const button = input.nextElementSibling;
        button.setAttribute('disabled', 'true');
        button.textContent = 'Booked';
    }
});

// Add click event listeners for booking buttons
document.querySelectorAll('.book-button').forEach(button => {
    button.addEventListener('click', () => {
        const date = button.getAttribute('data-date');
        const slot = button.getAttribute('data-slot');
        const input = document.querySelector(`input[data-date="${date}"][data-slot="${slot}"]`);
        const name = input.value.trim();

        if (name === '' || name.toLowerCase() === 'free') {
            alert('Name cannot be empty or "free"');
            return;
        }

        fetch('/book', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'day': date,
                'slot': slot,
                'name': name
            })
        }).then(response => response.json()).then(data => {
            if (data.status === 'success') {
                input.setAttribute('readonly', 'true');
                button.setAttribute('disabled', 'true');
                button.textContent = 'Booked';
            } else {
                alert(data.message);
            }
        }).catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });
});

// Function to update slots
function updateSlots(data) {
    for (const [key, value] of Object.entries(data)) {
        const [day, slot] = key.split('_');
        const slotId = `${day}-${slot}`;
        const input = document.getElementById(slotId);
        if (input) {
            if (value.toLowerCase() === 'free') {
                input.value = '';
                input.placeholder = 'free';
                input.removeAttribute('readonly');
                const button = input.nextElementSibling;
                button.removeAttribute('disabled');
                button.textContent = 'Book';
            } else {
                input.value = value;
                input.setAttribute('readonly', 'true');
                const button = input.nextElementSibling;
                button.setAttribute('disabled', 'true');
                button.textContent = 'Booked';
            }
        }
    }
}
