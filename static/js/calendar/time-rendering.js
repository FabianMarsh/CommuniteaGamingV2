export function renderAvailableTimes(times, selectedDate) {
  const timesList = document.getElementById("availableTimes");
  timesList.innerHTML = "";

  if (times.length === 0) {
    timesList.innerHTML = "<li class='no-times'>No available times for this date.</li>";
    return;
  }

  times.forEach(slot => {
    const li = document.createElement("li");
    li.innerText = slot.time.slice(0, 5);
    li.onclick = () => {
      document.getElementById("selected-time-field").value = slot.time;
      document.getElementById("selected-date-field").value = selectedDate;
      document.getElementById("booking-form").submit();
    };
    timesList.appendChild(li);
  });
}

export function highlightBookedTimes(selectedDate) {
  const baseUrl = window.location.origin;

  fetch(`${baseUrl}/bookings/get_booked_times/?date=${selectedDate}`)
    .then(res => res.json())
    .then(data => {
      const bookedTimes = data.times || [];

      document.querySelectorAll(".fc-timegrid-col").forEach(col => {
        const colDate = col.getAttribute("data-date");

        col.querySelectorAll(".fc-timegrid-slot").forEach(slot => {
          const timeAttr = slot.getAttribute("data-time");
          if (colDate === selectedDate && bookedTimes.includes(timeAttr)) {
            slot.classList.add("fc-timeslot-unavailable");
          }
        });
      });
    })
    .catch(err => {
      console.error("Failed to fetch booked times:", err);
    });
}
