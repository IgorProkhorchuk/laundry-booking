Simple website to book a timeslot for a laundry in the hotel



### Display Weekdays with Dates (Monday - Friday)

- Get the current date;
- Calculate the dates for Monday to Friday of the current week;
- Display these dates;


### Display Timeslots under Each Weekday

- Fetch all the data from the database and display the timeslots;
- Display these timeslots under each weekday;

### Display Box for Name under Each Timeslot

- if 'name' contain "free" - Create an input box for each respective timeslot to input the name;
- else - display the 'name';

### Display Button - Book under Each Timeslot

- Create a button labeled "Book" under each box;
- Button should be disabled and named "Booked" under each booked timeslot;

### Booking Confirmations

- Check if the name is entered in the respective timeslot before allowing booking;
- prevent to input incorrect name (contains only numbers);
- Display confirmation upon successful booking;

### Deactivate Button and Name Box After Booking

- Disable the "Book" button after booking
- Make the name box read-only, showing the entered name

### Switch Dates to Upcoming Week Every Saturday

- Implement a function that updates the dates to the upcoming week every Friday 8pm;
