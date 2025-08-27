import { showLoading, hideLoading } from "../../utils/loading.js";
import { loadAvailability } from "./availability-fetching.js";

export function setupSaveBlocks() {
  const saveBtn = document.getElementById("saveChanges");
  if (!saveBtn) return;

  saveBtn.addEventListener("click", () => {
    const date = document.getElementById("datePicker").value;
    if (!date) {
      alert("Please select a date.");
      return;
    }

    const checkboxes = document.querySelectorAll(".block-checkbox");
    const updates = Array.from(checkboxes).map(cb => ({
      time: cb.dataset.time,
      is_blocked: cb.checked
    }));

    const baseUrl = window.location.origin;

    showLoading();

    fetch(`${baseUrl}/bookings/apply_update_blocks/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ date, updates })
    })
      .then(res => {
        if (!res.ok) throw new Error("Failed to update blocks");
        return res.json();
      })
      .then(() => loadAvailability(date))
      .catch(err => {
        console.error("Error saving block changes:", err);
        alert("Could not save changes. Please try again.");
      })
      .finally(hideLoading);
  });
}

export function setupBlockUnblockButtons() {
  const blockBtn = document.getElementById("blockDay");
  const unblockBtn = document.getElementById("unblockDay");

  if (blockBtn) {
    blockBtn.addEventListener("click", () => {
      document.querySelectorAll(".block-checkbox").forEach(cb => cb.checked = true);
    });
  }

  if (unblockBtn) {
    unblockBtn.addEventListener("click", () => {
      document.querySelectorAll(".block-checkbox").forEach(cb => cb.checked = false);
    });
  }
}
