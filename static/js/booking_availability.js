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
    loadAvailability();
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
  dateInput.addEventListener("change", loadAvailability);
});

function loadAvailability() {
  const date = document.getElementById("datePicker").value;
  if (!date) {
    alert("Please select a date first.");
    return;
  }

  const baseUrl = window.location.origin;

  fetch(`${baseUrl}/bookings/availability_matrix/?date=${date}`)
    .then(res => res.json())
    .then(data => renderTable(data))
    .catch(err => {
      console.error("Error loading availability:", err);
      document.getElementById("availabilityTable").innerHTML =
        "<p>Could not load availability. Please try again.</p>";
    });
}

function renderTable(data) {
  const container = document.getElementById("availabilityTable");
  container.innerHTML = "";

  const matrix = data.matrix.map(row => ({
    ...row,
    available_seats: row.available_seats,
    is_hired: row.is_hired,
    is_blocked: row.is_blocked
  }));

  const table = document.createElement("table");
  table.classList.add("availability");

  // Header row
  const header = document.createElement("tr");
  header.innerHTML = `
    <th>Time Slot</th>
    <th>Seats</th>
    <th>Private Hire</th>
    <th>Block</th>
  `;
  table.appendChild(header);

  // Data rows
  matrix.forEach(row => {
    const tr = document.createElement("tr");

    const timeCell = `<td>${row.time}</td>`;
    const seatsCell = `<td>${row.available_seats}</td>`;
    const hireCell = `<td>${row.is_hired ? "Hired" : "Open"}</td>`;
    const blockCell = `
      <td>
        <input type="checkbox" data-time="${row.time}" ${row.is_blocked ? "checked" : ""}>
      </td>
    `;

    tr.innerHTML = timeCell + seatsCell + hireCell + blockCell;
    table.appendChild(tr);
  });

  container.appendChild(table);
}