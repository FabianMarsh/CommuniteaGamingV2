import { closeModal, bindOpenButton, bindCloseButton, bindDeleteButton, openEditModal, openViewModal } from "./modals/modal-utils.js";
import { initCalendar } from "./calendar/calendar-init.js";
import { fetchIsAdmin } from "./utils/user-access.js";

let isAdmin = false

document.addEventListener("DOMContentLoaded", () => {
  // Modal close buttons
  fetchIsAdmin().then(result => {
    isAdmin = result;

    // Now you can use isAdmin below
    setupModals();
    setupEditForm();
    setupCalendar();
  });
});

function setupModals() {
  bindCloseButton("view-modal");
  bindCloseButton("editModal");
  bindCloseButton("addModal");
  bindOpenButton("addEventBtn", "addModal");
  bindDeleteButton("deleteEventBtn", "editModal", "/events/delete");
}

function setupEditForm() {
  if (!isAdmin) return;
  const editForm = document.getElementById("editEventForm");
  if (!editForm) {
    console.error("Error: Edit event form not found!");
    return;
  }

  editForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const eventId = document.getElementById("editEventId")?.value;
    const formData = new FormData(this);

    if (!eventId) {
      console.error("Missing event ID for edit submission");
      return;
    }

    fetch(`/events/edit/${eventId}/`, {
      method: "POST",
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        console.log(data.message);
        closeModal("editModal");
        location.reload();
      })
      .catch(error => console.error("Error updating event:", error));
  });
}

// TODO add loading
function setupCalendar() {
  const calendarEl = document.getElementById("calendar");
  if (!calendarEl) return;

  initCalendar(calendarEl, {
    initialView: window.innerWidth >= 800 ? "timeGridWeek" : "dayGridDay",
    expandRows: true,
    contentHeight: "auto",
    events: "/events/json/",
    eventClick: info => {
      if (isAdmin) {
        if (info.event.id) {
          openEditModal({
            id: info.event.id,
            title: info.event.title,
            description: info.event.extendedProps.description,
            date: info.event.start.toISOString().split("T")[0],
            startTime: info.event.start.toLocaleString("en-GB", { hour: "2-digit", minute: "2-digit" }),
            endTime: info.event.end.toLocaleString("en-GB", { hour: "2-digit", minute: "2-digit" })
          });
        } else {
          console.error("Event ID is missing!");
        }
      } else {
        openViewModal({
          title: info.event.title,
          description: info.event.extendedProps.description,
          startTime: info.event.start.toLocaleString("en-GB", { hour: "2-digit", minute: "2-digit" }),
          endTime: info.event.end.toLocaleString("en-GB", { hour: "2-digit", minute: "2-digit" })
        });
      }
    },
    dateClick: info => {
      console.log("Clicked date:", info.dateStr);
    }
  });
}


