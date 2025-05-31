document.addEventListener("DOMContentLoaded", function () {
    const calendarEl = document.getElementById("calendar");
    const timesList = document.getElementById("available-times");

    if (!calendarEl || !timesList) return;

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        selectable: true,
        dateClick: function(info) {
            let selectedDate = info.dateStr;
            let today = new Date().toISOString().split("T")[0];

            if (selectedDate < today) {
                timesList.innerHTML = "";
                return;
            }

            const baseUrl = window.location.origin;
            let now = new Date();
            let currentTime = now.toTimeString().slice(0, 5) + ":00";

            // Fetch all available times
            fetch(`${baseUrl}/bookings/get_available_times/`)
                .then(response => response.json())
                .then(availableData => {
                    let allTimes = availableData.times;

                    // Fetch booked times for the selected date
                    fetch(`${baseUrl}/bookings/get_booked_times/?date=${selectedDate}`)
                        .then(response => response.json())
                        .then(bookedData => {
                            const bookedTimes = bookedData.times;

                            // Filter out booked times and past times for today's date
                            let filteredTimes = allTimes.filter(time => {
                                let isBooked = bookedTimes.includes(time);
                                let isPast = selectedDate === today && time < currentTime;
                                return !isBooked && !isPast;
                            });

                            timesList.innerHTML = "";

                            if (filteredTimes.length === 0) {
                                timesList.innerHTML = "<li>No available times for this date.</li>";
                                return;
                            }

                            // Populate available time slots dynamically
                            filteredTimes.forEach(time => {
                                let listItem = document.createElement("li");
                                listItem.innerText = time;

                                listItem.onclick = function() {
                                    document.getElementById("selected-time-field").value = time;
                                    document.getElementById("selected-date-field").value = selectedDate;
                                    document.getElementById("booking-form").submit();
                                };

                                timesList.appendChild(listItem);
                            });
                        });
                });
        }
    });

    calendar.render();
});


// restrict available times height
document.addEventListener("DOMContentLoaded", function () {
    function adjustMenuHeight() {
        const calendar = document.getElementById("calendar");
        const menu = document.getElementById("time-slot-menu");

        if (calendar && menu) {
            menu.style.maxHeight = calendar.clientHeight + "px";
        }
    }

    window.addEventListener("resize", adjustMenuHeight);
    adjustMenuHeight();
});

