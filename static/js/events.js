document.addEventListener("DOMContentLoaded", function () {
    var calendarEl = document.getElementById("calendar");

    if (!calendarEl) {
        console.error("Calendar element not found!");
        return;
    }

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        events: "/events/events/"
    });

    calendar.render();
    
});

