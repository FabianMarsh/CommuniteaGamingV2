import { showLoading, hideLoading } from "../utils/loading.js";
import { renderAvailableTimes } from "./time-rendering.js";

export function loadAvailableTimes(selectedDate) {
  const baseUrl = window.location.origin;
  const selectedSeats = parseInt(document.getElementById("selected-table-seats").value) || 0;
  const today = new Date().toISOString().split("T")[0];
  const now = new Date();
  const currentTime = now.toTimeString().slice(0, 5) + ":00";

  if (selectedDate < today) {
    document.getElementById("availableTimes").innerHTML = "";
    return;
  }

  showLoading();

  fetch(`${baseUrl}/bookings/get_available_times/?date=${selectedDate}`)
    .then(res => res.json())
    .then(data => {
      const filtered = data.times.filter(slot => {
        const isPast = selectedDate === today && slot.time < currentTime;
        const enoughSeats = slot.available_seats >= selectedSeats;
        return !isPast && enoughSeats && !slot.is_blocked;
      });

      renderAvailableTimes(filtered, selectedDate);
    })
    .catch(err => {
      console.error("Failed to fetch available times:", err);
      document.getElementById("availableTimes").innerHTML = "<li>Failed to load times.</li>";
    })
    .finally(hideLoading);
}
