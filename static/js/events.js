print("connected")
document.addEventListener("DOMContentLoaded", function () {
    var calendarEl = document.getElementById("calendar");

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        events: "/events/events/"  // Fetch events dynamically from Django
    });

    calendar.render();
});
