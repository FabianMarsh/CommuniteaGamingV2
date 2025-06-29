document.addEventListener("DOMContentLoaded", function () {
    const calendarEl = document.getElementById("calendar");
    const timesList = document.getElementById("available-times");

    if (!calendarEl || !timesList) return;

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        selectable: true,
        dateClick: function (info) {
            const selectedDate = info.dateStr;
            const today = new Date().toISOString().split("T")[0];
            const now = new Date();
            const currentTime = now.toTimeString().slice(0, 5) + ":00";

            if (selectedDate < today) {
                timesList.innerHTML = "";
                return;
            }

            const selectedSeats = parseInt(document.getElementById("selected-table-seats").value) || 0;
            const baseUrl = window.location.origin;

            fetch(`${baseUrl}/bookings/get_available_times/?date=${selectedDate}`)
                .then(response => response.json())
                .then(data => {
                    const filteredTimes = data.times.filter(slot => {
                        const isPast = selectedDate === today && slot.time < currentTime;
                        const enoughSeats = slot.available_seats >= selectedSeats;
                        return !isPast && enoughSeats;
                    });

                    timesList.innerHTML = "";

                    if (filteredTimes.length === 0) {
                        timesList.innerHTML = "<li>No available times for this date.</li>";
                        return;
                    }

                    filteredTimes.forEach(slot => {
                        const listItem = document.createElement("li");
                        listItem.innerText = `${slot.time.slice(0, 5)}`;

                        listItem.onclick = function () {
                            document.getElementById("selected-time-field").value = slot.time;
                            document.getElementById("selected-date-field").value = selectedDate;
                            document.getElementById("booking-form").submit();
                        };

                        timesList.appendChild(listItem);
                    });
                })
                .catch(error => {
                    console.error("Failed to fetch available times:", error);
                    timesList.innerHTML = "<li>Failed to load times. Please try again.</li>";
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

