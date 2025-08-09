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

  if (!data.matrix || data.matrix.length === 0) {
    container.innerHTML = "<p>No availability data found for this date.</p>";
    return;
  }

  const table = document.createElement("table");
  table.classList.add("availability");

  // Build header row
  const header = document.createElement("tr");
  header.innerHTML = `<th>Time</th><th>Availability</th>`;
  table.appendChild(header);

  // Build each time slot row
  data.matrix.forEach(row => {
    const tr = document.createElement("tr");
    let statusCell;

    if (row.is_blocked) {
      statusCell = `<td class="blocked">Private Hire</td>`;
    } else if (row.available_seats === 0) {
      statusCell = `<td class="full">Full</td>`;
    } else {
      statusCell = `<td>${row.available_seats} seats</td>`;
    }

    tr.innerHTML = `<td>${row.time}</td>${statusCell}`;
    table.appendChild(tr);
  });

  container.appendChild(table);
}
