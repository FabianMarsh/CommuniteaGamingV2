import { showLoading, hideLoading } from "../utils/loading.js";

// Fetch bookings for a given date
export function loadBookingsByDate(dateStr) {
  const baseUrl = window.location.origin;
  return fetch(`${baseUrl}/bookings/view_bookings/by_date/?date=${dateStr}`)
    .then(res => res.json());
}

// Optional: wrap loading + rendering if you want to centralise it
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

