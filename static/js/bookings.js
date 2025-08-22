import { show_loading, hide_loading } from "./loading.js";

document.addEventListener("DOMContentLoaded", function () {
  const calendarEl = document.getElementById("calendar");
  if (!calendarEl) return;

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "dayGridMonth",
    selectable: true,
    contentHeight: 'auto',
    slotMinTime: '12:00:00',
    slotMaxTime: '21:00:00',
    allDaySlot: false,
    selectAllow: function (selectInfo) {
      return selectInfo.start >= new Date();
    },
    dateClick: function (info) {
      const today = new Date().toISOString().split("T")[0];
      const clickedDate = info.dateStr;
      if (clickedDate < today) return;
      loadAvailableTimes(clickedDate);
    }
  });

  calendar.on('datesSet', function(info) {
    const selectedDate = info.startStr.split("T")[0];
    const baseUrl = window.location.origin;

    fetch(`${baseUrl}/bookings/get_booked_times/?date=${selectedDate}`)
      .then(response => response.json())
      .then(data => {
        const bookedTimes = data.times || [];

        document.querySelectorAll('.fc-timegrid-col').forEach(col => {
          const colDate = col.getAttribute('data-date');

          col.querySelectorAll('.fc-timegrid-slot').forEach(slot => {
            const timeAttr = slot.getAttribute('data-time');
            if (!colDate || !timeAttr) return;

            if (colDate === selectedDate && bookedTimes.includes(timeAttr)) {
              slot.classList.add('fc-timeslot-unavailable');
            }
          });
        });
      })
      .catch(error => {
        console.error("Failed to fetch booked times:", error);
      });
  });

  calendar.render();
});


function loadAvailableTimes(selectedDate) {
    const timesList = document.getElementById("available-times");
    const today = new Date().toISOString().split("T")[0];
    const now = new Date();
    const currentTime = now.toTimeString().slice(0, 5) + ":00";
    const selectedSeats = parseInt(document.getElementById("selected-table-seats").value) || 0;
    const baseUrl = window.location.origin;

    if (selectedDate < today) {
        timesList.innerHTML = "";
        return;
    }

    show_loading()

    fetch(`${baseUrl}/bookings/get_available_times/?date=${selectedDate}`)
        .then(response => response.json())
        .then(data => {
            const filteredTimes = data.times.filter(slot => {
                const isPast = selectedDate === today && slot.time < currentTime;
                const enoughSeats = slot.available_seats >= selectedSeats;
                const isBlocked = slot.is_blocked; 

                return !isPast && enoughSeats && !isBlocked;
            });

            timesList.innerHTML = "";

            if (filteredTimes.length === 0) {
                timesList.innerHTML = "<li class='no_times'>No available times for this date.</li>";
                hide_loading()
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
            hide_loading()
        })
        .catch(error => {
            console.error("Failed to fetch available times:", error);
            timesList.innerHTML = "<li>Failed to load times. Please try again.</li>";
            hide_loading()
        });
}


function enableTimeSlotSelection(calendar) {
    calendar.on('select', function(info) {
        const selectedDate = info.startStr.split("T")[0];
        const selectedTime = info.startStr.split("T")[1].slice(0,5) + ":00";
        document.getElementById("selected-time-field").value = selectedTime;
        document.getElementById("selected-date-field").value = selectedDate;
        document.getElementById("booking-form").submit();
    });
}

// restrict available times height
// document.addEventListener("DOMContentLoaded", function () {
//     function adjustMenuHeight() {
//         const calendar = document.getElementById("calendar");
//         const menu = document.getElementById("time-slot-menu");

//         if (calendar && menu) {
//             menu.style.maxHeight = calendar.clientHeight + "px";
//         }
//     }

//     window.addEventListener("resize", adjustMenuHeight);
//     adjustMenuHeight();
// });

