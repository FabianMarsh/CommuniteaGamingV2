document.addEventListener("DOMContentLoaded", function () {
    var calendarEl = document.getElementById("calendar");

    // ✅ Ensure calendar element exists before initializing
    if (!calendarEl) {
        console.error("Calendar element not found!");
        return;
    }

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        selectable: true,
        dateClick: function(info) {
            var selectedDate = info.dateStr;
            
            const baseUrl = window.location.origin; // needed until website is live
            // ✅ Fetch available times for the selected date
            fetch(`${baseUrl}/bookings/get_available_times/${selectedDate}`)
                .then(response => response.json())
                .then(data => {
                    console.log("Fetched Times:", data.times);  // ✅ Debugging step

                    var timesList = document.getElementById("available-times");
                    timesList.innerHTML = ""; // Clear previous times

                    if (data.times.length === 0) {
                        timesList.innerHTML = "<li>No available times for this date.</li>";
                        return;
                    }

                    // ✅ Set selected date in hidden form field
                    document.getElementById("selected-date-field").value = selectedDate;

                    data.times.forEach(time => {
                        var listItem = document.createElement("li");
                        listItem.innerText = time;

                        // ✅ Set form data and submit when a time is selected
                        listItem.onclick = function() {
                            document.getElementById("selected-time-field").value = time;
                            document.getElementById("booking-form").submit();
                        };

                        timesList.appendChild(listItem);
                    });
                })
                .catch(error => console.error("Error fetching times:", error));
        }
    });

    calendar.render(); // ✅ Render calendar
});


document.getElementById("available-times").addEventListener("click", function(event) {
    if (event.target.tagName === "LI") {
        let selectedTime = event.target.innerText;
        let selectedDate = document.getElementById("selected-date").innerText;  // ✅ Get selected date

        // ✅ Set form values
        document.getElementById("selected-date-field").value = selectedDate;
        document.getElementById("selected-time-field").value = selectedTime;

        // ✅ Submit form to `select_date_time`
        document.getElementById("booking-form").submit();
    }
});



