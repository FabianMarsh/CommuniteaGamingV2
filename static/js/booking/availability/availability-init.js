import { loadAvailability } from "./availability-fetching.js";
import { setupSaveBlocks, setupBlockUnblockButtons } from "./availability-actions.js";
import { formatDate, shiftDate } from "../../utils/date.js";

export function initAvailabilityPage() {
  const dateInput = document.getElementById("datePicker");
  const prevBtn = document.getElementById("datePrev");
  const nextBtn = document.getElementById("dateNext");

  if (!dateInput) return;

  dateInput.value = formatDate(new Date());
  loadAvailability(dateInput.value);

  prevBtn.addEventListener("click", () => {
    dateInput.value = shiftDate(dateInput.value, -1);
    dateInput.dispatchEvent(new Event("change"));
  });

  nextBtn.addEventListener("click", () => {
    dateInput.value = shiftDate(dateInput.value, 1);
    dateInput.dispatchEvent(new Event("change"));
  });

  dateInput.addEventListener("change", () => {
    loadAvailability(dateInput.value);
  });

  setupSaveBlocks();
  setupBlockUnblockButtons();
}
