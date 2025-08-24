// Open a modal by ID
export function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.classList.add("active");
}

// Close a modal by ID
export function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.classList.remove("active");
}

// Bind open button and Modal
export function bindOpenButton(buttonId, modalId) {
  const btn = document.getElementById(buttonId);
  if (btn) {
    btn.addEventListener("click", () => openModal(modalId));
  }
}

// Bind a close button inside a modal
export function bindCloseButton(modalId, closeSelector = ".close") {
  const modal = document.getElementById(modalId);
  if (!modal) return;

  const closeBtn = modal.querySelector(closeSelector);
  if (closeBtn) {
    closeBtn.addEventListener("click", () => closeModal(modalId));
  }
}

// Inject data and open the edit modal
export function openEditModal({ id, title, description, date, startTime, endTime }) {
  const fields = {
    "editEventId": id,
    "editTitle": title,
    "editDescription": description,
    "editDate": date,
    "editStartTime": startTime,
    "editEndTime": endTime
  };

  for (const [fieldId, value] of Object.entries(fields)) {
    const el = document.getElementById(fieldId);
    if (el) el.value = value;
    else console.warn(`Missing field: ${fieldId}`);
  }

  openModal("editModal");
}

// Inject data and open the view modal
export function bindDeleteButton(buttonId, modalId, endpointBase) {
  const btn = document.getElementById(buttonId);
  if (!btn) return;

  btn.addEventListener("click", () => {
    const eventId = document.getElementById("editEventId")?.value;
    if (!eventId) return;

    if (confirm("Are you sure you want to delete this event?")) {
      fetch(`${endpointBase}/${eventId}/`, { method: "DELETE" })
        .then(res => res.json())
        .then(data => {
          console.log(data.message);
          closeModal(modalId);
          location.reload();
        })
        .catch(err => console.error("Error deleting event:", err));
    }
  });
}


// Inject data and open the view modal
export function openViewModal({ title, description, startTime, endTime }) {
  document.getElementById("title").textContent = title || "Untitled";
  document.getElementById("description").textContent = description || "No description";
  document.getElementById("start_time").innerHTML = `<strong>Start Time: </strong>${startTime}`;
  document.getElementById("end_time").innerHTML = `<strong>End Time: </strong>${endTime}`;
  openModal("view-modal");
}
