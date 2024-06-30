const socket = io();

socket.on('init_bookings', function(data) {
    updateSlots(data);
});

socket.on('update_bookings', function(data) {
    const slotId = `${data.day}-${data.slot}`;
    const input = document.getElementById(slotId);
    input.value = data.name;
    input.setAttribute('readonly', 'true');
    const button = input.nextElementSibling;
    button.setAttribute('disabled', 'true');
    button.textContent = 'Booked';
});

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
        });
    });
});

function updateSlots(data) {
    for (const [key, value] of Object.entries(data)) {
        const [day, slot] = key.split('_');
        const slotId = `${day}-${slot}`;
        const input = document.getElementById(slotId);
        if (input) {
            input.value = value;
            if (value === '' || value.toLowerCase() === 'free') {
                input.removeAttribute('readonly');
                const button = input.nextElementSibling;
                button.removeAttribute('disabled');
                button.textContent = 'Book';
            } else {
                input.setAttribute('readonly', 'true');
                const button = input.nextElementSibling;
                button.setAttribute('disabled', 'true');
                button.textContent = 'Booked';
            }
        }
    }
}
