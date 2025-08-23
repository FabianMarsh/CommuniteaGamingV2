import { show_loading, hide_loading } from "./loading.js";


document.addEventListener("DOMContentLoaded", () => {
  const dateInput = document.getElementById("datePicker");
  const prevBtn = document.getElementById("datePrev");
  const nextBtn = document.getElementById("dateNext");

  // Helper to format date as YYYY-MM-DD
  const formatDate = (dateObj) => {
    const yyyy = dateObj.getFullYear();
    const mm = String(dateObj.getMonth() + 1).padStart(2, "0");
    const dd = String(dateObj.getDate()).padStart(2, "0");
    return `${yyyy}-${mm}-${dd}`;
  };

  // Set today's date and load availability
  if (dateInput) {
    const today = new Date();
    dateInput.value = formatDate(today);
    loadBookings();
  }

  // Shift date by ±1 day and trigger availability reload
  const shiftDate = (direction) => {
    if (!dateInput.value) return;
    const currentDate = new Date(dateInput.value);
    currentDate.setDate(currentDate.getDate() + direction);
    dateInput.value = formatDate(currentDate);
    dateInput.dispatchEvent(new Event("change"));
  };

  prevBtn.addEventListener("click", () => shiftDate(-1));
  nextBtn.addEventListener("click", () => shiftDate(1));

  // Load availability when date changes
  dateInput.addEventListener("change", loadBookings);
});

document.querySelector('.close-button').addEventListener('click', () => {
  document.getElementById('bookingModal').classList.remove('active');
});

function loadBookings() {
  const date = document.getElementById("datePicker").value;
  if (!date) {
    alert("Please select a date first.");
    return;
  }

  const baseUrl = window.location.origin;
  const table = document.getElementById("bookingsTable");

  show_loading();

  fetch(`${baseUrl}/bookings/view_bookings/by_date/?date=${date}`)
    .then(res => res.json())
    .then(data => {
      renderTable(data); // This should now expect a single day's bookings
    })
    .catch(err => {
      console.error("Error loading bookings:", err);
      table.innerHTML = "<p>Could not load bookings. Please try again.</p>";
    })
    .finally(() => {
      hide_loading();
    });
}



function renderTable(data) {
  const container = document.getElementById("bookingsTable");
  container.innerHTML = "";

  const table = document.createElement("table");
  table.classList.add("bookings");

  const timeSlots = data.matrix.map(slot => slot.timeslot);

  // Header row
  const header = document.createElement("tr");
  timeSlots.forEach(time => {
    const th = document.createElement("th");
    th.textContent = time;
    header.appendChild(th);
  });
  table.appendChild(header);

  const maxRows = Math.max(...data.matrix.map(slot => slot.bookings.length));

  for (let i = 0; i < maxRows; i++) {
    const tr = document.createElement("tr");

    data.matrix.forEach(slot => {
      const td = document.createElement("td");
      const booking = slot.bookings[i];

      if (booking) {
        td.innerHTML = `
          ${booking.table_name}<br>
          ${booking.name}<br>
          ${booking.table_name.toLowerCase().includes("private") 
            ? (booking.paid ? "Paid" : "Not paid") 
            : ""}
        `;

        td.classList.add("booking-cell");
        td.dataset.bookingId = booking.id;

        td.addEventListener("click", () => {
          console.log("click"); // ✅ Should now log
          const modalDetails = document.getElementById("modalDetails");
          modalDetails.innerHTML = `
            <strong>Table:</strong> ${booking.table_name}<br>
            <strong>Name:</strong> ${booking.name}<br>
            <strong>Email:</strong> ${booking.email}<br>
            <strong>Phone:</strong> ${booking.phone}<br>
            <strong>Paid:</strong> ${
                booking.table_name.toLowerCase().includes("private")
                    ? (booking.paid ? "Paid" : "Not paid")
                    : (booking.paid ? "Yes" : "No")
            }<br>
            <strong>Notes:</strong> ${booking.notes ? booking.notes : "No Notes"}
          `;
          document.getElementById("bookingModal").classList.add("active");
        });

      } else {
        td.innerHTML = "";
      }

      tr.appendChild(td);
    });

    table.appendChild(tr);
  }

  container.appendChild(table);
}
