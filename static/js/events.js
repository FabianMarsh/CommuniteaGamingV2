// READ functionality ----------------------------------

// Retrieve
document.addEventListener("DOMContentLoaded", function () {
    var calendarEl = document.getElementById("calendar");

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        events: "/events/json/",
        eventClick: function(info) {
            alert("Event: " + info.event.title + "\nDescription: " + info.event.extendedProps.description);
        },
    });

    calendar.render();
});

// Edit

document.addEventListener("DOMContentLoaded", function () {
    var editForm = document.getElementById("edit-event-form");
    if (editForm) {
        editForm.addEventListener("submit", function(event) {
            event.preventDefault();
            var eventId = document.getElementById("edit-event-id").value;
            var formData = new FormData(this);

            fetch(`/events/edit/${eventId}/`, {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                closeEditModal();
                location.reload(); // Refresh events after edit
            })
            .catch(error => console.error("Error updating event:", error));
        });
    } else {
        console.error("Error: Edit event form not found!");
    }
});

// Add

document.addEventListener("DOMContentLoaded", function () {
    var calendarEl = document.getElementById("calendar");

    fetch("/events/user/is_admin/")  // Check if the user is an admin
        .then(response => response.json())
        .then(data => {
            var isAdmin = data.is_admin;

            var calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: "dayGridMonth",
                events: "/events/json/",
                eventClick: function(info) {
                    if (isAdmin) {
                        if (info.event.id) {
                            openEditModal(
                                info.event.id,
                                info.event.title,
                                info.event.extendedProps.description,
                                info.event.start.toISOString().split("T")[0],
                                info.event.start.toISOString().split("T")[1].slice(0, 5),
                                info.event.end ? info.event.end.toISOString().split("T")[1].slice(0, 5) : ""
                            );
                        } else {
                            console.error("Event ID is missing!");
                        }
                    }
                },
                dateClick: function(info) {
                    console.log("Clicked date:", info.dateStr);
                }
            });

            calendar.render();

            if (isAdmin) {
                setTimeout(() => {
                    document.querySelectorAll(".fc-event").forEach(eventElement => {
                        var editButton = document.createElement("button");
                        editButton.classList.add("edit-event-btn");
                        editButton.textContent = "Edit";
                        editButton.classList.add("edit-event-btn");

                        editButton.onclick = function () {
                            var eventId = eventElement.getAttribute("data-event-id");
                            var event = calendar.getEventById(eventId);
                            if (event) {
                                openEditModal(
                                    event.id,
                                    event.title,
                                    event.extendedProps.description,
                                    event.start.toISOString().split("T")[0],
                                    event.start.toISOString().split("T")[1].slice(0, 5),
                                    event.end.toISOString().split("T")[1].slice(0, 5)
                                );
                            }
                        };

                        eventElement.appendChild(editButton);
                    });
                }, 500);  // Wait for FullCalendar to render events before modifying DOM
            }
        })
        .catch(error => console.error("Error checking admin status:", error));
});

// Delete

document.addEventListener("DOMContentLoaded", function () {
    var deleteButton = document.getElementById("delete-event-btn");

    if (deleteButton) {
        deleteButton.addEventListener("click", function () {
            var eventId = document.getElementById("edit-event-id").value;

            if (confirm("Are you sure you want to delete this event?")) {
                fetch(`/events/delete/${eventId}/`, {
                    method: "DELETE"
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data.message);
                    closeEditModal();
                    location.reload(); // Refresh events after deletion
                })
                .catch(error => console.error("Error deleting event:", error));
            }
        });
    } else {
        console.error("Error: Delete Event button not found!");
    }
});



// Modals ----------------------------------

document.addEventListener("DOMContentLoaded", function () {
    var modal = document.getElementById("add-modal");
    var openBtn = document.getElementById("add-event-btn");
    var closeBtn = document.querySelector(".close");

    openBtn.addEventListener("click", function () {
        modal.style.display = "block";
    });

    closeBtn.addEventListener("click", function () {
        modal.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});

function openEditModal(id, title, description, date, start_time, end_time) {
    document.getElementById("edit-event-id").value = id;  // **Set the event ID here**
    document.getElementById("edit-title").value = title;
    document.getElementById("edit-description").value = description;
    document.getElementById("edit-date").value = date;
    document.getElementById("edit-start-time").value = start_time;
    document.getElementById("edit-end-time").value = end_time;

    document.getElementById("edit-modal").style.display = "block";
}


function closeEditModal() {
    document.getElementById("edit-modal").style.display = "none";
}
