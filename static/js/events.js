
// READ functionality ----------------------------------

// Retrieve
document.addEventListener("DOMContentLoaded", function () {
  const calendarEl = document.getElementById("calendar");

  fetch("/events/user/is_admin/")
    .then(response => response.json())
    .then(data => {
        const isAdmin = data.is_admin;
        const screenWidth = window.innerWidth;
        let initialView = screenWidth >= 768 ? (isAdmin ? "timeGridWeek" : "dayGridDay"): "timeGridDay";
        
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
                openEditModal(
                    info.event.id,
                    info.event.title,
                    info.event.extendedProps.description,
                    info.event.start.toISOString().split("T")[0],
                    info.event.start.toLocaleString("en-GB", { hour: "2-digit", minute: "2-digit" }),
                    info.event.end ? info.event.end.toLocaleString("en-GB", { hour: "2-digit", minute: "2-digit" }) : ""
                );
                } else {
                console.error("Event ID is missing!");
                }
            } else {
                alert(
                "Event: " + info.event.title +
                "\nDescription: " + info.event.extendedProps.description
                );
            }
            },
            dateClick: function (info) {
            console.log("Clicked date:", info.dateStr);
            }
        });

        calendar.render();
        });
});


// Edit

document.addEventListener("DOMContentLoaded", function () {
  const editForm = document.getElementById("edit-event-form");

  if (editForm) {
    editForm.addEventListener("submit", function (event) {
      event.preventDefault();
      const eventId = document.getElementById("edit-event-id").value;
      const formData = new FormData(this);

      fetch(`/events/edit/${eventId}/`, {
        method: "POST",
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          console.log(data.message);
          closeEditModal();
          location.reload(); // Refresh calendar
        })
        .catch(error => console.error("Error updating event:", error));
    });
  } else {
    console.error("Error: Edit event form not found!");
  }
});

// Add

document.addEventListener("DOMContentLoaded", function () {
  const addForm = document.getElementById("add-event-form");

  if (addForm) {
    addForm.addEventListener("submit", function (event) {
      event.preventDefault();

      const formData = new FormData(this);

      fetch("/events/add/", {
        method: "POST",
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          console.log(data.message);
          closeAddModal(); // Optional: if you’re using a modal for adding
          location.reload(); // Refresh calendar to show new event
        })
        .catch(error => console.error("Error adding event:", error));
    });
  } else {
    console.error("Error: Add event form not found!");
  }
});


// Delete

document.addEventListener("DOMContentLoaded", function () {
  const deleteButton = document.getElementById("delete-event-btn");

  if (deleteButton) {
    deleteButton.addEventListener("click", function () {
      const eventId = document.getElementById("edit-event-id").value;

      if (confirm("Are you sure you want to delete this event?")) {
        fetch(`/events/delete/${eventId}/`, {
          method: "DELETE",
        })
          .then(response => response.json())
          .then(data => {
            console.log(data.message);
            closeEditModal();
            location.reload(); // Refresh calendar
          })
          .catch(error => console.error("Error deleting event:", error));
      }
    });
  } else {
    console.error("Error: Delete Event button not found!");
  }
});




// Modals ----------------------------------

// Add

document.addEventListener("DOMContentLoaded", function () {
    var modal = document.getElementById("add-modal");
    var openBtn = document.getElementById("add-event-btn");
    var closeBtn = document.querySelector(".close");

    // Open modal function
    openBtn.addEventListener("click", function () {
        modal.classList.add("active");
    });

    // Close modal function
    closeBtn.addEventListener("click", function () {
        modal.classList.remove("active");
    });
});

// Edit

document.addEventListener("DOMContentLoaded", function () {
    var modal = document.getElementById("edit-modal");
    var closeBtn = document.querySelector(".close");

    // Close modal function
    closeBtn.addEventListener("click", function () {
        modal.classList.remove("active");
    });
});

document.addEventListener("DOMContentLoaded", function () {
    var editModal = document.getElementById("edit-modal");
    
    var closeBtn = editModal.querySelector(".close");

    // Function to open edit modal
    function openEditModal(id, title, description, date, start_time) {

        document.getElementById("edit-event-id").value = id;
        document.getElementById("edit-title").value = title;
        document.getElementById("edit-description").value = description;
        document.getElementById("edit-date").value = date;
        document.getElementById("edit-start-time").value = start_time;

        editModal.classList.add("active");
    }

    // Close modal when clicking close button
    if (closeBtn) {
        closeBtn.addEventListener("click", function () {
            closeEditModal();
        });
    }

    // Make `openEditModal` globally accessible
    window.openEditModal = openEditModal;
});


function closeEditModal() {
    var editModal = document.getElementById("edit-modal");
    if (editModal) {
        editModal.classList.remove("active");
    }
}
