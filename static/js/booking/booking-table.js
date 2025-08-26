// Render the booking table
export function renderBookingTable(data, containerId = "bookingsTable") {
  const container = document.getElementById(containerId);
  container.innerHTML = "";

  if (!data.matrix || data.matrix.length === 0) {
    container.innerHTML = "<p>No bookings available for this date.</p>";
    return;
  }

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
      const booking = slot.bookings[i];
      const td = createBookingCell(booking);
      tr.appendChild(td);
    });

    table.appendChild(tr);
  }

  container.appendChild(table);
}

// Create a single booking cell
function createBookingCell(booking) {
  const td = document.createElement("td");

  if (booking) {
    td.innerHTML = `
      ${booking.table_name}<br>
      ${booking.name}<br>
      ${getPaidLabel(booking)}
    `;
    td.classList.add("booking-cell");
    td.dataset.bookingId = booking.id;
    td.addEventListener("click", () => bindBookingModal(booking));
  }

  return td;
}

// Determine paid label based on table type
function getPaidLabel(booking) {
  const isPrivate = booking.table_name.toLowerCase().includes("private");
  if (isPrivate) {
    return booking.paid ? "Paid" : "Not paid";
  }
  return booking.paid ? "Yes" : "No";
}

// Populate and show modal with booking details
export function bindBookingModal(booking) {
  const modalDetails = document.getElementById("modalDetails");
  modalDetails.innerHTML = `
    <span><strong>Table:</strong> ${booking.table_name}</span><br>
    <span><strong>Name:</strong> ${booking.name}</span><br>
    <span><strong>Email:</strong> ${booking.email}</span><br>
    <span><strong>Phone:</strong> ${booking.phone}</span><br>
    <span><strong>Paid:</strong> ${getPaidLabel(booking)}</span><br>
    <span><strong>Notes:</strong> ${booking.notes ? booking.notes : "No Notes"}</span>
  `;
  document.getElementById("bookingModal").classList.add("active");
}