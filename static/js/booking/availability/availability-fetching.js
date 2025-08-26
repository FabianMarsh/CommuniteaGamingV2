import { showLoading, hideLoading } from "../../utils/loading.js";
import { renderAvailabilityTable } from "./availability-rendering.js";

export function loadAvailability(date) {
  const baseUrl = window.location.origin;
  const table = document.getElementById("availabilityTable");

  showLoading();

  fetch(`${baseUrl}/bookings/availability_matrix/?date=${date}`)
    .then(res => res.json())
    .then(data => renderAvailabilityTable(data))
    .catch(err => {
      console.error("Error loading availability:", err);
      table.innerHTML = "<p>Could not load availability. Please try again.</p>";
    })
    .finally(hideLoading);
}
