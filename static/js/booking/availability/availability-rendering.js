export function renderAvailabilityTable(data) {
  const container = document.getElementById("availabilityTable");
  container.innerHTML = "";

  const matrix = data.matrix;

  const table = document.createElement("table");
  table.classList.add("availability");

  const header = document.createElement("tr");
  header.innerHTML = `
    <th>Time Slot</th>
    <th>Seats</th>
    <th>Private Hire</th>
    <th>Blocked</th>
  `;
  table.appendChild(header);

  matrix.forEach(row => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.time}</td>
      <td>${row.available_seats}</td>
      <td>${row.is_hired ? "Hired" : "Open"}</td>
      <td>
        <input type="checkbox" class="block-checkbox" data-time="${row.time}" ${row.is_blocked ? "checked" : ""}>
      </td>
    `;
    table.appendChild(tr);
  });

  container.appendChild(table);
}
