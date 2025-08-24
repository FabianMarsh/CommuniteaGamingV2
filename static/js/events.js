import { openModal, closeModal, bindOpenButton, bindCloseButton, bindDeleteButton, openEditModal, openViewModal } from "./modals/modal-utils.js";

document.addEventListener("DOMContentLoaded", () => {
  // Modal close buttons
  bindCloseButton("view-modal");
  bindCloseButton("editModal");
  bindCloseButton("addModal");

  // Modal open buttons
  bindOpenButton("addEventBtn", "addModal");

  // Delete button inside edit modal
  bindDeleteButton("deleteEventBtn", "editModal", "/events/delete");

  // Edit form submission
  const editForm = document.getElementById("editEventForm");
  if (editForm) {
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
  } else {
    console.error("Error: Edit event form not found!");
  }
});


// Retrieve
document.addEventListener("DOMContentLoaded", function () {
  const calendarEl = document.getElementById("calendar");

  /* TODO importable is_admin fetch */
  fetch("/events/user/is_admin/")
    .then(response => response.json())
    .then(data => {
      const isAdmin = data.is_admin;
      const screenWidth = window.innerWidth;
      let initialView = screenWidth >= 800 ? "timeGridWeek" : "dayGridDay";

      const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: initialView,
        slotMinTime: "12:00:00",
        slotMaxTime: "22:00:00",
        expandRows: true,
        contentHeight: "auto",
        events: "/events/json/",
        eventClick: function (info) {
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
        dateClick: function (info) {
          console.log("Clicked date:", info.dateStr);
        }
      });

      calendar.render();
    });
});

