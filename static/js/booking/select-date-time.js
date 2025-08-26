import { initCalendar } from "../calendar/calendar-init.js";
import { loadAvailableTimes } from "../calendar/time-fetching.js";
import { highlightBookedTimes } from "../calendar/time-rendering.js";

document.addEventListener("DOMContentLoaded", () => {
  const calendarEl = document.getElementById("calendar");

  initCalendar(calendarEl, {
    initialView: "dayGridMonth",
    selectable: true,
    slotMaxTime: "21:00:00",
    allDaySlot: false,
    selectAllow: info => info.start >= new Date(),
    dateClick: info => {
      const today = new Date().toISOString().split("T")[0];
      if (info.dateStr >= today) {
        loadAvailableTimes(info.dateStr);
      }
    },
    datesSet: info => {
      const selectedDate = info.startStr.split("T")[0];
      highlightBookedTimes(selectedDate);
    }
  });
});

