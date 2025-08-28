import { showLoading, hideLoading } from "../utils/loading.js";

// Fetch bookings for a given date
export function loadBookingsByDate(dateStr) {
  const baseUrl = window.location.origin;
  return fetch(`${baseUrl}/bookings/bookings_by_date/?date=${dateStr}`)
    .then(res => res.json());
}

export function loadAndRenderBookings(dateStr, renderFn) {
  showLoading();
  loadBookingsByDate(dateStr)
    .then(data => renderFn(data))
    .catch(err => {
      console.error("Error loading bookings:", err);
      document.getElementById("bookingsTable").innerHTML = "<p>Could not load bookings.</p>";
    })
    .finally(hideLoading);
}

