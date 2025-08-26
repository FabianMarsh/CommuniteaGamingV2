export function initCalendar(calendarEl, config = {}) {
  if (!calendarEl) return;

  const screenWidth = window.innerWidth;
  const defaultView = config.initialView || (screenWidth >= 800 ? "timeGridWeek" : "dayGridDay");

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: defaultView,
    contentHeight: "auto",
    slotMinTime: config.slotMinTime || "12:00:00",
    slotMaxTime: config.slotMaxTime || "22:00:00",
    expandRows: config.expandRows || false,
    selectable: config.selectable || false,
    allDaySlot: config.allDaySlot || false,
    events: config.events || null,
    selectAllow: config.selectAllow || null,
    dateClick: config.dateClick || null,
    eventClick: config.eventClick || null,
    datesSet: config.datesSet || null
  });

  calendar.render();
}

