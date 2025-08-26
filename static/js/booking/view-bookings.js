import { formatDate, shiftDate } from "../utils/date.js";
import { loadAndRenderBookings } from "../booking/booking-utils.js";
import { renderBookingTable } from "../booking/booking-table.js";

document.addEventListener("DOMContentLoaded", () => {
  const dateInput = document.getElementById("datePicker");
  const prevBtn = document.getElementById("datePrev");
  const nextBtn = document.getElementById("dateNext");

  if (!dateInput) return;

  dateInput.value = formatDate(new Date());
  loadAndRenderBookings(dateInput.value, renderBookingTable);

  prevBtn.addEventListener("click", () => {
    dateInput.value = shiftDate(dateInput.value, -1);
    dateInput.dispatchEvent(new Event("change"));
  });

  nextBtn.addEventListener("click", () => {
    dateInput.value = shiftDate(dateInput.value, 1);
    dateInput.dispatchEvent(new Event("change"));
  });

  dateInput.addEventListener("change", () => {
    loadAndRenderBookings(dateInput.value, renderBookingTable);
  });

  document.querySelector(".close").addEventListener("click", () => {
    document.getElementById("bookingModal").classList.remove("active");
  });
});